import logging
import os
import re
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    DATASET_CONFIG,
    EMBEDDINGS_CONFIG,
    LLM_CONFIG,
    LOGGING_CONFIG,
    RETRIEVER_CONFIG,
)


# ==================================================
# ENVIRONMENT
# ==================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "dataset.csv"
)

VECTORDB_PATH = (
    BASE_DIR
    / "faiss_index"
)

LOG_FILE_PATH = (
    BASE_DIR
    / LOGGING_CONFIG["log_file"]
)


# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=getattr(
        logging,
        LOGGING_CONFIG["level"],
    ),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(
            LOG_FILE_PATH,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# ==================================================
# RETRIEVAL CONFIGURATION
# ==================================================

MAX_RETRIEVAL_CANDIDATES = 8

# Minimum score required for the best source.
MIN_BEST_RELEVANCE = 0.30

# Secondary sources must be reasonably close
# to the strongest source.
ADDITIONAL_SOURCE_RATIO = 0.88

MIN_ADDITIONAL_RELEVANCE = 0.46

MAX_SOURCES = 3


# ==================================================
# TEXT NORMALIZATION
# ==================================================

def normalize_text(text):
    """
    Normalize text for lexical comparison.

    Converts text to lowercase and extracts
    alphanumeric tokens.
    """
    return re.findall(
        r"\b[a-z0-9]+\b",
        str(text).lower(),
    )


def normalize_phrase(text):
    """
    Normalize text while preserving word order.

    Used for phrase matching.
    """
    text = str(text).lower()

    # Normalize common contractions.
    replacements = {
        "won't": "will not",
        "can't": "cannot",
        "doesn't": "does not",
        "isn't": "is not",
        "wasn't": "was not",
        "don't": "do not",
        "didn't": "did not",
        "couldn't": "could not",
        "wouldn't": "would not",
        "shouldn't": "should not",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new,
        )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ==================================================
# LEXICAL SCORE
# ==================================================

def calculate_lexical_overlap(
    query,
    document_text,
):
    """
    Calculate the proportion of meaningful query
    terms found in a document.

    Stop words are ignored so words such as:
    'what', 'should', 'I', 'do', 'if'
    do not dominate retrieval.
    """

    stop_words = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "am",
        "was",
        "were",
        "be",
        "been",
        "being",
        "i",
        "me",
        "my",
        "we",
        "our",
        "you",
        "your",
        "they",
        "their",
        "what",
        "which",
        "who",
        "where",
        "when",
        "why",
        "how",
        "do",
        "does",
        "did",
        "should",
        "could",
        "would",
        "can",
        "will",
        "if",
        "to",
        "for",
        "of",
        "on",
        "in",
        "at",
        "with",
        "and",
        "or",
        "but",
        "about",
        "please",
        "tell",
        "me",
    }

    query_terms = {
        term
        for term in normalize_text(query)
        if term not in stop_words
        and len(term) > 1
    }

    document_terms = set(
        normalize_text(document_text)
    )

    if not query_terms:
        return 0.0

    matched_terms = (
        query_terms.intersection(
            document_terms
        )
    )

    return (
        len(matched_terms)
        / len(query_terms)
    )


# ==================================================
# PHRASE MATCHING
# ==================================================

def generate_ngrams(
    text,
    n,
):
    """
    Generate normalized word n-grams.
    """
    words = normalize_phrase(
        text
    ).split()

    if len(words) < n:
        return set()

    return {
        " ".join(words[index:index + n])
        for index in range(
            len(words) - n + 1
        )
    }


def calculate_phrase_match(
    query,
    document_text,
):
    """
    Calculate phrase-level similarity.

    Exact two-word and three-word phrases receive
    stronger importance than individual words.

    This is particularly useful for support queries such as:

    - turn on
    - unusual noise
    - filter replacement
    - refund request
    - customer support
    """

    normalized_query = normalize_phrase(
        query
    )

    normalized_document = normalize_phrase(
        document_text
    )

    if not normalized_query:
        return 0.0

    # Strong exact phrase match.
    if (
        normalized_query in normalized_document
        and len(normalized_query.split()) >= 2
    ):
        return 1.0

    query_bigrams = generate_ngrams(
        normalized_query,
        2,
    )

    document_bigrams = generate_ngrams(
        normalized_document,
        2,
    )

    query_trigrams = generate_ngrams(
        normalized_query,
        3,
    )

    document_trigrams = generate_ngrams(
        normalized_document,
        3,
    )

    bigram_score = 0.0
    trigram_score = 0.0

    if query_bigrams:
        bigram_score = (
            len(
                query_bigrams.intersection(
                    document_bigrams
                )
            )
            / len(query_bigrams)
        )

    if query_trigrams:
        trigram_score = (
            len(
                query_trigrams.intersection(
                    document_trigrams
                )
            )
            / len(query_trigrams)
        )

    # Trigrams are more specific than bigrams.
    return max(
        bigram_score,
        trigram_score,
    )


# ==================================================
# ISSUE / INTENT KEYWORD MATCHING
# ==================================================

def calculate_intent_match(
    query,
    document_text,
):
    """
    Detect important customer-service intent phrases.

    This gives a controlled boost to documents that contain
    the same troubleshooting intent as the question.

    It does NOT generate factual information.
    It only affects retrieval ranking.
    """

    query_text = normalize_phrase(
        query
    )

    document_text = normalize_phrase(
        document_text
    )

    if not query_text:
        return 0.0

    intent_groups = [
        {
            "name": "power_on",
            "query_phrases": [
                "turn on",
                "turn the device on",
                "device will not turn on",
                "device won't turn on",
                "does not turn on",
                "will not turn on",
                "power on",
                "power up",
                "not turning on",
                "doesn't turn on",
            ],
            "document_phrases": [
                "turn on",
                "turn the device on",
                "device will not turn on",
                "device won't turn on",
                "does not turn on",
                "will not turn on",
                "power on",
                "power up",
                "not turning on",
            ],
        },
        {
            "name": "noise",
            "query_phrases": [
                "unusual noise",
                "strange noise",
                "weird noise",
                "making noise",
                "loud noise",
            ],
            "document_phrases": [
                "unusual noise",
                "strange noise",
                "weird noise",
                "making noise",
                "loud noise",
            ],
        },
        {
            "name": "filter",
            "query_phrases": [
                "filter replacement",
                "replace filter",
                "filter needs replacement",
                "filter indicator",
            ],
            "document_phrases": [
                "filter replacement",
                "replace filter",
                "filter indicator",
                "filter should normally be replaced",
            ],
        },
        {
            "name": "refund",
            "query_phrases": [
                "refund request",
                "request a refund",
                "refund",
                "refund eligibility",
            ],
            "document_phrases": [
                "refund request",
                "refund",
                "refund eligibility",
            ],
        },
        {
            "name": "warranty",
            "query_phrases": [
                "warranty",
                "warranty coverage",
                "covered by warranty",
            ],
            "document_phrases": [
                "warranty",
                "warranty coverage",
                "covered by warranty",
            ],
        },
        {
            "name": "support",
            "query_phrases": [
                "customer support",
                "contact support",
                "customer service",
                "support team",
            ],
            "document_phrases": [
                "customer support",
                "contact support",
                "customer service",
                "support team",
            ],
        },
    ]

    matched_intents = []

    for group in intent_groups:
        query_match = any(
            phrase in query_text
            for phrase in group[
                "query_phrases"
            ]
        )

        if not query_match:
            continue

        document_match = any(
            phrase in document_text
            for phrase in group[
                "document_phrases"
            ]
        )

        if document_match:
            matched_intents.append(
                group["name"]
            )

    if matched_intents:
        return 1.0

    return 0.0


# ==================================================
# COMBINED RELEVANCE
# ==================================================

def calculate_combined_relevance(
    semantic_score,
    lexical_score,
    phrase_score=0.0,
    intent_score=0.0,
):
    """
    Combine semantic, lexical, phrase, and intent
    relevance signals.

    Ranking priority:

    1. Semantic similarity
    2. Exact phrase matching
    3. Intent matching
    4. Individual keyword overlap

    The intent and phrase signals are especially useful
    for short troubleshooting questions.
    """

    semantic_score = max(
        0.0,
        min(
            1.0,
            float(semantic_score),
        ),
    )

    lexical_score = max(
        0.0,
        min(
            1.0,
            float(lexical_score),
        ),
    )

    phrase_score = max(
        0.0,
        min(
            1.0,
            float(phrase_score),
        ),
    )

    intent_score = max(
        0.0,
        min(
            1.0,
            float(intent_score),
        ),
    )

    # Semantic similarity remains important,
    # while exact support phrases receive a strong boost.
    return (
        semantic_score * 0.50
        + phrase_score * 0.20
        + intent_score * 0.20
        + lexical_score * 0.10
    )


# ==================================================
# LLM
# ==================================================

@lru_cache(maxsize=1)
def get_llm():
    """
    Initialize and cache the Gemini LLM.
    """

    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not configured. "
            "Add it to the .env file or Streamlit secrets."
        )

    llm = ChatGoogleGenerativeAI(
        model=LLM_CONFIG["model"],
        google_api_key=api_key,
        max_tokens=LLM_CONFIG[
            "max_tokens"
        ],
    )

    logger.info(
        "Gemini LLM initialized"
    )

    return llm


# ==================================================
# EMBEDDINGS
# ==================================================

@lru_cache(maxsize=1)
def get_embeddings():
    """
    Load and cache HuggingFace embeddings.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG[
            "model_name"
        ]
    )

    logger.info(
        "Embeddings model loaded"
    )

    return embeddings


# ==================================================
# CREATE VECTOR DATABASE
# ==================================================

def create_vector_db():
    """
    Create and save the FAISS vector database
    from the current dataset.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}"
        )

    loader = CSVLoader(
        file_path=str(
            DATASET_PATH
        ),
        source_column=DATASET_CONFIG[
            "csv_column"
        ],
    )

    documents = loader.load()

    if not documents:
        raise ValueError(
            "The dataset does not contain any documents."
        )

    embeddings = get_embeddings()

    vectordb = FAISS.from_documents(
        documents,
        embeddings,
    )

    VECTORDB_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    vectordb.save_local(
        str(VECTORDB_PATH)
    )

    load_vector_db.cache_clear()

    logger.info(
        "FAISS vector database created with %d documents",
        len(documents),
    )

    return vectordb


# ==================================================
# LOAD VECTOR DATABASE
# ==================================================

@lru_cache(maxsize=1)
def load_vector_db():
    """
    Load the existing FAISS vector database.
    """

    if not VECTORDB_PATH.exists():
        raise FileNotFoundError(
            f"Vector database not found at {VECTORDB_PATH}. "
            "Please create it first."
        )

    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    logger.info(
        "Loaded FAISS index with %d vectors",
        vectordb.index.ntotal,
    )

    return vectordb


# ==================================================
# BUILD PROMPT
# ==================================================

def _build_prompt():
    """
    Build the customer-service RAG prompt.
    """

    return ChatPromptTemplate.from_template(
        """
You are a helpful customer service assistant.

Answer the current question using ONLY the information
provided in the knowledge-base context.

You may use the previous conversation to understand
what the user is referring to.

Do not use the previous conversation as a source of facts.
The knowledge-base context is the only source of factual information.

If the answer is not present in the knowledge-base context,
say exactly:

"I don't know based on the available information."

Do not make up information.

Give the answer clearly and directly.
When the knowledge base provides steps, preserve the
important steps in a numbered list.

Previous conversation:
{history}

Knowledge-base context:
{context}

Current question:
{question}
"""
    )


# ==================================================
# HISTORY FORMATTER
# ==================================================

def _prepare_history(
    chat_history,
):
    """
    Convert recent conversation messages into text.
    """

    chat_history = chat_history or []

    history_messages = chat_history[
        -6:
    ]

    history_text = "\n".join(
        f"{message.get('role', 'user').capitalize()}: "
        f"{message.get('content', '')}"
        for message in history_messages
        if message.get("content")
    )

    return (
        history_text
        or "No previous conversation."
    )


# ==================================================
# RETRIEVAL
# ==================================================

def _retrieve_documents(
    question,
    chat_history=None,
):
    """
    Retrieve and rank relevant documents.

    IMPORTANT:
    Retrieval scoring uses the CURRENT QUESTION for
    lexical, phrase, and intent matching.

    Conversation history is used only to help semantic
    retrieval understand follow-up questions.

    This prevents unrelated previous messages from
    dominating keyword matching.
    """

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": MAX_RETRIEVAL_CANDIDATES,
        }
    )

    history_text = _prepare_history(
        chat_history
    )

    retrieval_query = question

    if history_text != "No previous conversation.":
        retrieval_query = (
            "Previous conversation:\n"
            f"{history_text}\n\n"
            "Current question:\n"
            f"{question}"
        )

    logger.info(
        "Question: %s",
        question,
    )

    logger.info(
        "Retrieval query prepared."
    )

    # ------------------------------------------
    # Candidate retrieval
    # ------------------------------------------

    candidate_documents = (
        retriever.invoke(
            retrieval_query
        )
    )

    # ------------------------------------------
    # Semantic scores
    # ------------------------------------------

    scored_results = []

    try:
        scored_results = (
            vectordb.similarity_search_with_relevance_scores(
                retrieval_query,
                k=MAX_RETRIEVAL_CANDIDATES,
            )
        )
    except Exception as error:
        logger.warning(
            "Could not obtain normalized semantic scores: %s",
            error,
        )

    scored_documents = []

    # ------------------------------------------
    # Primary scoring
    # ------------------------------------------

    if scored_results:

        for document, semantic_score in scored_results:

            page_content = (
                document.page_content
            )

            lexical_score = (
                calculate_lexical_overlap(
                    question,
                    page_content,
                )
            )

            phrase_score = (
                calculate_phrase_match(
                    question,
                    page_content,
                )
            )

            intent_score = (
                calculate_intent_match(
                    question,
                    page_content,
                )
            )

            relevance_score = (
                calculate_combined_relevance(
                    semantic_score,
                    lexical_score,
                    phrase_score,
                    intent_score,
                )
            )

            # Save detailed scores inside metadata.
            document.metadata[
                "semantic_score"
            ] = round(
                float(
                    semantic_score
                ),
                4,
            )

            document.metadata[
                "lexical_score"
            ] = round(
                float(
                    lexical_score
                ),
                4,
            )

            document.metadata[
                "phrase_score"
            ] = round(
                float(
                    phrase_score
                ),
                4,
            )

            document.metadata[
                "intent_score"
            ] = round(
                float(
                    intent_score
                ),
                4,
            )

            document.metadata[
                "relevance_score"
            ] = round(
                float(
                    relevance_score
                ),
                4,
            )

            scored_documents.append(
                (
                    document,
                    float(
                        semantic_score
                    ),
                    float(
                        lexical_score
                    ),
                    float(
                        phrase_score
                    ),
                    float(
                        intent_score
                    ),
                    float(
                        relevance_score
                    ),
                )
            )

    # ------------------------------------------
    # Fallback scoring
    # ------------------------------------------

    if not scored_documents:

        for rank, document in enumerate(
            candidate_documents
        ):

            page_content = (
                document.page_content
            )

            lexical_score = (
                calculate_lexical_overlap(
                    question,
                    page_content,
                )
            )

            phrase_score = (
                calculate_phrase_match(
                    question,
                    page_content,
                )
            )

            intent_score = (
                calculate_intent_match(
                    question,
                    page_content,
                )
            )

            # Approximate semantic ordering when
            # normalized scores are unavailable.
            semantic_score = max(
                0.0,
                1.0
                - (
                    rank
                    / max(
                        len(
                            candidate_documents
                        ),
                        1,
                    )
                ),
            )

            relevance_score = (
                calculate_combined_relevance(
                    semantic_score,
                    lexical_score,
                    phrase_score,
                    intent_score,
                )
            )

            document.metadata[
                "semantic_score"
            ] = round(
                float(
                    semantic_score
                ),
                4,
            )

            document.metadata[
                "lexical_score"
            ] = round(
                float(
                    lexical_score
                ),
                4,
            )

            document.metadata[
                "phrase_score"
            ] = round(
                float(
                    phrase_score
                ),
                4,
            )

            document.metadata[
                "intent_score"
            ] = round(
                float(
                    intent_score
                ),
                4,
            )

            document.metadata[
                "relevance_score"
            ] = round(
                float(
                    relevance_score
                ),
                4,
            )

            scored_documents.append(
                (
                    document,
                    semantic_score,
                    lexical_score,
                    phrase_score,
                    intent_score,
                    relevance_score,
                )
            )

    # ------------------------------------------
    # Sort by final relevance
    # ------------------------------------------

    scored_documents.sort(
        key=lambda item: item[5],
        reverse=True,
    )

    # ------------------------------------------
    # Log top results
    # ------------------------------------------

    for rank, item in enumerate(
        scored_documents[:5],
        start=1,
    ):

        document = item[0]

        logger.info(
            "Retrieval candidate %d | "
            "semantic=%.4f | lexical=%.4f | "
            "phrase=%.4f | intent=%.4f | "
            "relevance=%.4f | text=%s",
            rank,
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
            document.page_content[
                :100
            ].replace(
                "\n",
                " ",
            ),
        )

    # ------------------------------------------
    # Select relevant documents
    # ------------------------------------------

    selected_documents = []

    if scored_documents:

        (
            best_document,
            best_semantic,
            best_lexical,
            best_phrase,
            best_intent,
            best_relevance,
        ) = scored_documents[0]

        # --------------------------------------
        # Special protection:
        # If there is a strong exact phrase or
        # intent match, trust it even when the
        # embedding similarity is not perfect.
        # --------------------------------------

        strong_exact_match = (
            best_phrase >= 0.50
            or best_intent >= 1.0
        )

        if (
            best_relevance
            >= MIN_BEST_RELEVANCE
            or strong_exact_match
        ):
            selected_documents.append(
                best_document
            )

            # ----------------------------------
            # Secondary sources
            # ----------------------------------

            for item in scored_documents[1:]:

                if (
                    len(selected_documents)
                    >= MAX_SOURCES
                ):
                    break

                (
                    document,
                    _semantic_score,
                    _lexical_score,
                    _phrase_score,
                    _intent_score,
                    relevance_score,
                ) = item

                # A secondary source must be both
                # relevant and reasonably close to
                # the strongest source.
                if (
                    relevance_score
                    >= MIN_ADDITIONAL_RELEVANCE
                    and relevance_score
                    >= (
                        best_relevance
                        * ADDITIONAL_SOURCE_RATIO
                    )
                ):
                    selected_documents.append(
                        document
                    )

    # ------------------------------------------
    # Final retrieval log
    # ------------------------------------------

    logger.info(
        "Retrieved %d candidates; selected %d relevant sources.",
        len(scored_documents),
        len(selected_documents),
    )

    if selected_documents:

        for index, document in enumerate(
            selected_documents,
            start=1,
        ):

            logger.info(
                "Selected source %d: %s",
                index,
                document.page_content[
                    :150
                ].replace(
                    "\n",
                    " ",
                ),
            )

    return (
        selected_documents,
        history_text,
    )


# ==================================================
# PREPARE QA
# ==================================================

def _prepare_qa(
    question,
    chat_history=None,
):
    """
    Perform retrieval and prepare the Gemini prompt.
    """

    question = str(
        question
    ).strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    (
        selected_documents,
        history_text,
    ) = _retrieve_documents(
        question,
        chat_history,
    )

    # ------------------------------------------
    # No relevant source
    # ------------------------------------------

    if not selected_documents:

        return {
            "question": question,
            "history": history_text,
            "context": "",
            "messages": None,
            "source_documents": [],
            "has_context": False,
        }

    # ------------------------------------------
    # Build context
    # ------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in selected_documents
    )

    logger.info(
        "Context size: %d characters",
        len(context),
    )

    # ------------------------------------------
    # Prompt
    # ------------------------------------------

    prompt = _build_prompt()

    messages = prompt.invoke(
        {
            "history": history_text,
            "context": context,
            "question": question,
        }
    )

    return {
        "question": question,
        "history": history_text,
        "context": context,
        "messages": messages,
        "source_documents": selected_documents,
        "has_context": True,
    }


# ==================================================
# RESPONSE CONTENT NORMALIZATION
# ==================================================

def _extract_response_text(
    content,
):
    """
    Normalize Gemini response content into plain text.
    """

    if content is None:
        return ""

    if isinstance(
        content,
        str,
    ):
        return content

    if isinstance(
        content,
        list,
    ):

        text_parts = []

        for item in content:

            if isinstance(
                item,
                str,
            ):
                text_parts.append(
                    item
                )

            elif isinstance(
                item,
                dict,
            ):

                if "text" in item:
                    text_parts.append(
                        str(
                            item["text"]
                        )
                    )

        return "".join(
            text_parts
        )

    return str(content)


# ==================================================
# NORMAL QA CHAIN
# ==================================================

def get_qa_chain():
    """
    Create the customer-service RAG
    question-answering function.

    This function is retained for compatibility
    with tests and other project modules.
    """

    def ask_question(
        question,
        chat_history=None,
    ):

        prepared = _prepare_qa(
            question,
            chat_history,
        )

        # --------------------------------------
        # No relevant information
        # --------------------------------------

        if not prepared[
            "has_context"
        ]:

            return {
                "result": (
                    "I don't know based on "
                    "the available information."
                ),
                "source_documents": [],
            }

        # --------------------------------------
        # Generate response
        # --------------------------------------

        logger.info(
            "Generating response with Gemini..."
        )

        response = (
            get_llm().invoke(
                prepared["messages"]
            )
        )

        answer = _extract_response_text(
            response.content
        ).strip()

        return {
            "result": answer,
            "source_documents": prepared[
                "source_documents"
            ],
        }

    return ask_question


# ==================================================
# STREAMING QA
# ==================================================

def get_qa_stream(
    question,
    chat_history=None,
):
    """
    Prepare a RAG question and return:

        (stream_generator, source_documents)

    The generator yields Gemini response chunks
    so Streamlit can display the answer progressively.
    """

    prepared = _prepare_qa(
        question,
        chat_history,
    )

    # ------------------------------------------
    # No relevant source
    # ------------------------------------------

    if not prepared[
        "has_context"
    ]:

        def unknown_generator():
            yield (
                "I don't know based on "
                "the available information."
            )

        return (
            unknown_generator(),
            [],
        )

    # ------------------------------------------
    # Gemini streaming
    # ------------------------------------------

    def response_generator():

        logger.info(
            "Generating streaming response with Gemini..."
        )

        try:

            stream = (
                get_llm().stream(
                    prepared["messages"]
                )
            )

            for chunk in stream:

                content = getattr(
                    chunk,
                    "content",
                    "",
                )

                text = _extract_response_text(
                    content
                )

                if text:
                    yield text

        except Exception as error:

            logger.exception(
                "Streaming response failed: %s",
                error,
            )

            raise

    return (
        response_generator(),
        prepared[
            "source_documents"
        ],
    )


# ==================================================
# DEBUG / TEST
# ==================================================

if __name__ == "__main__":

    logger.info(
        "=" * 60
    )

    logger.info(
        "Customer Service Chatbot - Retrieval Test"
    )

    logger.info(
        "=" * 60
    )

    # ------------------------------------------
    # Rebuild vector database
    # ------------------------------------------

    create_vector_db()

    # ------------------------------------------
    # Test question
    # ------------------------------------------

    test_question = (
        "What should I do if the device "
        "won't turn on?"
    )

    logger.info(
        "Test question: %s",
        test_question,
    )

    # ------------------------------------------
    # Normal QA test
    # ------------------------------------------

    chain = get_qa_chain()

    result = chain(
        test_question
    )

    logger.info(
        "Answer: %s",
        result["result"],
    )

    logger.info(
        "Selected sources: %d",
        len(
            result[
                "source_documents"
            ]
        ),
    )

    for index, document in enumerate(
        result[
            "source_documents"
        ],
        start=1,
    ):

        logger.info(
            "Source %d: %s",
            index,
            document.page_content[
                :300
            ].replace(
                "\n",
                " ",
            ),
        )

    logger.info(
        "=" * 60
    )