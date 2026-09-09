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
)


# ==================================================
# ENVIRONMENT
# ==================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent

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

MIN_BEST_RELEVANCE = 0.30

ADDITIONAL_SOURCE_RATIO = 0.88

MIN_ADDITIONAL_RELEVANCE = 0.46

MAX_SOURCES = 3


# ==================================================
# TEXT NORMALIZATION
# ==================================================

def normalize_text(text):
    """
    Normalize text for lexical comparison.
    """

    return re.findall(
        r"\b[a-z0-9]+\b",
        str(text).lower(),
    )


def normalize_phrase(text):
    """
    Normalize text while preserving word order.
    """

    text = str(
        text
    ).lower()

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
    Calculate meaningful query-term overlap.
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
    }

    query_terms = {
        term
        for term in normalize_text(
            query
        )
        if term not in stop_words
        and len(term) > 1
    }

    document_terms = set(
        normalize_text(
            document_text
        )
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
# N-GRAMS
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
        " ".join(
            words[index:index + n]
        )
        for index in range(
            len(words) - n + 1
        )
    }


# ==================================================
# PHRASE MATCHING
# ==================================================

def calculate_phrase_match(
    query,
    document_text,
):
    """
    Calculate phrase-level similarity.
    """

    normalized_query = normalize_phrase(
        query
    )

    normalized_document = normalize_phrase(
        document_text
    )

    if not normalized_query:
        return 0.0

    if (
        normalized_query
        in normalized_document
        and len(
            normalized_query.split()
        ) >= 2
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

    return max(
        bigram_score,
        trigram_score,
    )


# ==================================================
# INTENT MATCHING
# ==================================================

def calculate_intent_match(
    query,
    document_text,
):
    """
    Detect support-related intent overlap.

    This affects retrieval ranking only.
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
    Combine retrieval signals.
    """

    semantic_score = max(
        0.0,
        min(
            1.0,
            float(
                semantic_score
            ),
        ),
    )

    lexical_score = max(
        0.0,
        min(
            1.0,
            float(
                lexical_score
            ),
        ),
    )

    phrase_score = max(
        0.0,
        min(
            1.0,
            float(
                phrase_score
            ),
        ),
    )

    intent_score = max(
        0.0,
        min(
            1.0,
            float(
                intent_score
            ),
        ),
    )

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
    Initialize and cache Gemini.
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
        "Gemini LLM initialized."
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
        "Embeddings model loaded."
    )

    return embeddings


# ==================================================
# GLOBAL VECTOR DATABASE
# ==================================================

def create_vector_db():
    """
    Create the global FAISS database from dataset.csv.
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

    vectordb = FAISS.from_documents(
        documents,
        get_embeddings(),
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
        "Global FAISS created with %d documents.",
        len(documents),
    )

    return vectordb


@lru_cache(maxsize=1)
def load_vector_db():
    """
    Load the global FAISS database.

    If it does not exist yet, create it automatically.
    """

    if not VECTORDB_PATH.exists():

        logger.info(
            "Global FAISS does not exist. Creating it automatically."
        )

        return create_vector_db()

    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    logger.info(
        "Loaded global FAISS with %d vectors.",
        vectordb.index.ntotal,
    )

    return vectordb


# ==================================================
# HISTORY
# ==================================================

def _prepare_history(
    chat_history,
):
    """
    Convert recent messages into text.
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
# RETRIEVAL CANDIDATES
# ==================================================

def _get_global_candidates(
    retrieval_query,
):
    """
    Retrieve candidates from the global knowledge base.
    """

    try:

        vectordb = load_vector_db()

        scored_results = (
            vectordb
            .similarity_search_with_relevance_scores(
                retrieval_query,
                k=MAX_RETRIEVAL_CANDIDATES,
            )
        )

        return scored_results

    except Exception as error:

        logger.warning(
            "Global retrieval failed: %s",
            error,
        )

        return []


def _get_conversation_candidates(
    chat_id,
    retrieval_query,
):
    """
    Retrieve candidates from the current chat's files.
    """

    if not chat_id:
        return []

    try:

        from src.conversation_files import (
            search_conversation_files,
        )

        return search_conversation_files(
            chat_id,
            retrieval_query,
            k=MAX_RETRIEVAL_CANDIDATES,
        )

    except Exception as error:

        logger.warning(
            "Conversation-file retrieval failed: %s",
            error,
        )

        return []


# ==================================================
# DOCUMENT SCORING
# ==================================================

def _score_documents(
    scored_results,
    question,
):
    """
    Apply the existing semantic + lexical +
    phrase + intent ranking system.
    """

    scored_documents = []

    for document, semantic_score in scored_results:

        try:

            semantic_score = float(
                semantic_score
            )

        except Exception:

            semantic_score = 0.0

        semantic_score = max(
            0.0,
            min(
                1.0,
                semantic_score,
            ),
        )

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

        metadata = document.metadata

        metadata["semantic_score"] = round(
            semantic_score,
            4,
        )

        metadata["lexical_score"] = round(
            lexical_score,
            4,
        )

        metadata["phrase_score"] = round(
            phrase_score,
            4,
        )

        metadata["intent_score"] = round(
            intent_score,
            4,
        )

        metadata["relevance_score"] = round(
            relevance_score,
            4,
        )

        if metadata.get(
            "source_type"
        ) == "conversation_file":

            metadata["source_type"] = (
                "conversation_file"
            )

        else:

            metadata.setdefault(
                "source_type",
                "global_knowledge",
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

    return scored_documents


# ==================================================
# RETRIEVE + RANK
# ==================================================

def _retrieve_documents(
    question,
    chat_history=None,
    chat_id=None,
):
    """
    Retrieve from BOTH:

    1. Global knowledge base
    2. Current conversation files

    Chat history helps semantic retrieval but does not
    participate in lexical / phrase / intent scoring.
    """

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

    # ----------------------------------------------
    # Global candidates
    # ----------------------------------------------

    global_results = _get_global_candidates(
        retrieval_query
    )

    # ----------------------------------------------
    # Conversation candidates
    # ----------------------------------------------

    conversation_results = (
        _get_conversation_candidates(
            chat_id,
            retrieval_query,
        )
    )

    # ----------------------------------------------
    # Combine
    # ----------------------------------------------

    combined_results = (
        global_results
        + conversation_results
    )

    # ----------------------------------------------
    # Deduplicate
    # ----------------------------------------------

    unique_results = []

    seen = set()

    for document, semantic_score in combined_results:

        metadata = document.metadata or {}

        file_id = metadata.get(
            "file_id",
            "",
        )

        content_key = (
            file_id,
            document.page_content.strip(),
        )

        if content_key in seen:
            continue

        seen.add(
            content_key
        )

        unique_results.append(
            (
                document,
                semantic_score,
            )
        )

    # ----------------------------------------------
    # Rank
    # ----------------------------------------------

    scored_documents = _score_documents(
        unique_results,
        question,
    )

    scored_documents.sort(
        key=lambda item: item[5],
        reverse=True,
    )

    # ----------------------------------------------
    # Log candidates
    # ----------------------------------------------

    for rank, item in enumerate(
        scored_documents[:5],
        start=1,
    ):

        document = item[0]

        logger.info(
            "Retrieval candidate %d | "
            "semantic=%.4f | lexical=%.4f | "
            "phrase=%.4f | intent=%.4f | "
            "relevance=%.4f | source=%s | text=%s",
            rank,
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
            document.metadata.get(
                "source_type",
                "global_knowledge",
            ),
            document.page_content[
                :100
            ].replace(
                "\n",
                " ",
            ),
        )

    # ----------------------------------------------
    # Select sources
    # ----------------------------------------------

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

    logger.info(
        "Retrieved %d candidates; selected %d sources.",
        len(scored_documents),
        len(selected_documents),
    )

    return (
        selected_documents,
        history_text,
    )


# ==================================================
# PROMPT
# ==================================================

def _build_prompt():
    """
    Build the RAG prompt.
    """

    return ChatPromptTemplate.from_template(
        """
You are a helpful customer service assistant.

Answer the current question using ONLY the information
provided in the knowledge-base context.

The knowledge-base context can contain:
- Global company knowledge
- Files uploaded by the user in this conversation

Treat both as factual sources.

You may use the previous conversation to understand
what the user is referring to.

Do not use previous conversation messages as factual
sources.

If the answer is not present in the knowledge-base
context, say exactly:

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
# PREPARE QA
# ==================================================

def _prepare_qa(
    question,
    chat_history=None,
    chat_id=None,
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
        chat_id,
    )

    if not selected_documents:

        return {
            "question": question,
            "history": history_text,
            "context": "",
            "messages": None,
            "source_documents": [],
            "has_context": False,
        }

    context = "\n\n".join(
        document.page_content
        for document in selected_documents
    )

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
# RESPONSE NORMALIZATION
# ==================================================

def _extract_response_text(
    content,
):
    """
    Normalize Gemini response content.
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

    return str(
        content
    )


# ==================================================
# NORMAL QA
# ==================================================

def get_qa_chain():
    """
    Return a compatible non-streaming QA function.
    """

    def ask_question(
        question,
        chat_history=None,
        chat_id=None,
    ):

        prepared = _prepare_qa(
            question,
            chat_history,
            chat_id,
        )

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
    chat_id=None,
):
    """
    Prepare a RAG question and return:

        (stream_generator, source_documents)

    The generator yields Gemini response chunks.
    """

    prepared = _prepare_qa(
        question,
        chat_history,
        chat_id,
    )

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
# DEBUG
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

    create_vector_db()

    test_question = (
        "What should I do if the device "
        "won't turn on?"
    )

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