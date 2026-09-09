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


# ============================================================
# ENVIRONMENT
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


# ============================================================
# PATHS
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

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


# ============================================================
# LOGGING
# ============================================================

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


# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

MAX_RETRIEVAL_CANDIDATES = 8

MIN_BEST_RELEVANCE = 0.25

MIN_ADDITIONAL_RELEVANCE = 0.38

ADDITIONAL_SOURCE_RATIO = 0.75

MAX_SOURCES = 5


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    return re.findall(
        r"\b[a-z0-9]+\b",
        str(text).lower(),
    )


def normalize_phrase(text):

    text = str(
        text or ""
    ).lower()

    replacements = {
        "won't": "will not",
        "can't": "cannot",
        "cannot": "can not",
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


# ============================================================
# LEXICAL SCORE
# ============================================================

def calculate_lexical_overlap(
    query,
    document_text,
):
    query_terms = set(
        normalize_text(
            query
        )
    )

    document_terms = set(
        normalize_text(
            document_text
        )
    )

    if not query_terms:
        return 0.0

    return (
        len(
            query_terms
            .intersection(
                document_terms
            )
        )
        / len(query_terms)
    )


# ============================================================
# N-GRAM SCORE
# ============================================================

def generate_ngrams(
    text,
    n,
):
    tokens = normalize_text(
        text
    )

    if len(tokens) < n:
        return set()

    return {
        " ".join(
            tokens[index:index + n]
        )
        for index in range(
            len(tokens) - n + 1
        )
    }


def calculate_phrase_match(
    query,
    document_text,
):
    query_phrase = normalize_phrase(
        query
    )

    document_phrase = normalize_phrase(
        document_text
    )

    if not query_phrase:
        return 0.0

    if query_phrase in document_phrase:
        return 1.0

    query_bigrams = generate_ngrams(
        query_phrase,
        2,
    )

    document_bigrams = generate_ngrams(
        document_phrase,
        2,
    )

    if not query_bigrams:
        return 0.0

    overlap = (
        query_bigrams
        .intersection(
            document_bigrams
        )
    )

    return len(overlap) / len(
        query_bigrams
    )


# ============================================================
# INTENT MATCHING
# ============================================================

INTENT_GROUPS = {

    "power_on": {
        "turn on",
        "turn off",
        "power",
        "won't turn on",
        "will not turn on",
        "not turning on",
        "does not turn on",
        "device won't start",
        "device will not start",
        "not starting",
    },

    "noise": {
        "noise",
        "noisy",
        "unusual noise",
        "strange noise",
        "sound",
        "loud",
        "vibration",
    },

    "filter": {
        "filter",
        "replace filter",
        "filter replacement",
        "hepa",
        "filter indicator",
        "red filter",
    },

    "refund": {
        "refund",
        "refund request",
        "money back",
        "return",
        "return product",
    },

    "warranty": {
        "warranty",
        "warranty period",
        "manufacturing defect",
        "physical damage",
    },

    "support": {
        "support",
        "customer support",
        "contact support",
        "help",
        "customer service",
    },
}


def calculate_intent_match(
    query,
    document_text,
):
    query_normalized = normalize_phrase(
        query
    )

    document_normalized = normalize_phrase(
        document_text
    )

    if not query_normalized:
        return 0.0

    best_score = 0.0

    for phrases in INTENT_GROUPS.values():

        query_hits = [
            phrase
            for phrase in phrases
            if normalize_phrase(
                phrase
            )
            in query_normalized
        ]

        if not query_hits:
            continue

        document_hits = [
            phrase
            for phrase in phrases
            if normalize_phrase(
                phrase
            )
            in document_normalized
        ]

        if document_hits:

            score = min(
                1.0,
                (
                    len(document_hits)
                    / max(
                        len(query_hits),
                        1,
                    )
                ),
            )

            best_score = max(
                best_score,
                score,
            )

    return best_score


# ============================================================
# COMBINED RELEVANCE
# ============================================================

def calculate_combined_relevance(
    semantic_score,
    lexical_score,
    phrase_score,
    intent_score,
):
    return (
        semantic_score * 0.50
        + phrase_score * 0.20
        + intent_score * 0.20
        + lexical_score * 0.10
    )


# ============================================================
# LLM
# ============================================================

@lru_cache(maxsize=1)
def get_llm():

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


# ============================================================
# EMBEDDINGS
# ============================================================

@lru_cache(maxsize=1)
def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG[
            "model_name"
        ]
    )

    logger.info(
        "Embeddings model loaded"
    )

    return embeddings


# ============================================================
# GLOBAL VECTOR DATABASE
# ============================================================

def create_vector_db():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found at "
            f"{DATASET_PATH}"
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
        "FAISS vector database created with %d documents",
        len(documents),
    )

    return vectordb


# ============================================================
# LOAD GLOBAL VECTOR DATABASE
# ============================================================

@lru_cache(maxsize=1)
def load_vector_db():

    if not VECTORDB_PATH.exists():

        raise FileNotFoundError(
            f"Vector database not found at "
            f"{VECTORDB_PATH}. "
            f"Please create it first."
        )

    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    logger.info(
        "Loaded global FAISS index with %d vectors",
        vectordb.index.ntotal,
    )

    return vectordb


# ============================================================
# CONVERSATION VECTOR DATABASE
# ============================================================

def load_conversation_vector_db(
    chat_id
):
    """
    Lazy import prevents circular import problems.

    conversation_files.py itself uses get_embeddings()
    from this module.
    """

    if not chat_id:
        return None

    try:

        from src.conversation_files import (
            load_conversation_vector_db as loader,
        )

        return loader(
            str(chat_id)
        )

    except Exception as error:

        logger.warning(
            "Could not load conversation FAISS: %s",
            error,
        )

        return None


# ============================================================
# DOCUMENT SEARCH
# ============================================================

def search_vector_db(
    vectordb,
    query,
    k=MAX_RETRIEVAL_CANDIDATES,
):
    if vectordb is None:
        return []

    try:

        return (
            vectordb
            .similarity_search_with_relevance_scores(
                query,
                k=k,
            )
        )

    except Exception as error:

        logger.warning(
            "Relevance-score search failed: %s",
            error,
        )

        try:

            documents = (
                vectordb
                .similarity_search(
                    query,
                    k=k,
                )
            )

            return [
                (
                    document,
                    max(
                        0.0,
                        1.0
                        - (
                            index
                            / max(
                                len(documents),
                                1,
                            )
                        ),
                    ),
                )
                for index, document
                in enumerate(
                    documents
                )
            ]

        except Exception as fallback_error:

            logger.error(
                "Vector search failed: %s",
                fallback_error,
            )

            return []


# ============================================================
# DOCUMENT ID
# ============================================================

def document_identity(
    document
):
    metadata = getattr(
        document,
        "metadata",
        {},
    )

    if not isinstance(
        metadata,
        dict,
    ):
        metadata = {}

    return (
        metadata.get(
            "source_file"
        )
        or metadata.get(
            "file_name"
        )
        or metadata.get(
            "filename"
        )
        or metadata.get(
            "source"
        )
        or ""
    ) + "|" + str(
        getattr(
            document,
            "page_content",
            "",
        )
    )[:250]


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(
    question,
    chat_history=None,
    chat_id=None,
):
    """
    Search BOTH knowledge sources:

    1. Global company knowledge base.
    2. Files attached to the current conversation.

    The two stores remain physically separate.
    """

    question = str(
        question or ""
    ).strip()

    if not question:
        return []

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    history_messages = (
        chat_history or []
    )[-6:]

    history_text = "\n".join(
        f"{message.get('role', '').capitalize()}: "
        f"{message.get('content', '')}"
        for message in history_messages
        if message.get(
            "content"
        )
    )

    # --------------------------------------------------------
    # SEMANTIC RETRIEVAL QUERY
    # --------------------------------------------------------

    retrieval_query = question

    if history_text:

        retrieval_query = (
            "Previous conversation:\n"
            f"{history_text}\n\n"
            "Current question:\n"
            f"{question}"
        )

    logger.info(
        "Retrieval started for question: %s",
        question,
    )

    # --------------------------------------------------------
    # GLOBAL SEARCH
    # --------------------------------------------------------

    global_db = None

    try:

        global_db = load_vector_db()

    except Exception as error:

        logger.warning(
            "Global vector database unavailable: %s",
            error,
        )

    global_results = search_vector_db(
        global_db,
        retrieval_query,
    )

    # --------------------------------------------------------
    # CONVERSATION FILE SEARCH
    # --------------------------------------------------------

    conversation_db = (
        load_conversation_vector_db(
            chat_id
        )
    )

    conversation_results = (
        search_vector_db(
            conversation_db,
            retrieval_query,
        )
    )

    logger.info(
        "Global candidates: %d",
        len(global_results),
    )

    logger.info(
        "Conversation-file candidates: %d",
        len(conversation_results),
    )

    # --------------------------------------------------------
    # COMBINE RESULTS
    # --------------------------------------------------------

    all_results = []

    for document, semantic_score in global_results:

        all_results.append(
            (
                document,
                float(
                    semantic_score
                ),
                "global_knowledge",
            )
        )

    for document, semantic_score in conversation_results:

        all_results.append(
            (
                document,
                float(
                    semantic_score
                ),
                "conversation_file",
            )
        )

    # --------------------------------------------------------
    # SCORE EVERY DOCUMENT
    # --------------------------------------------------------

    scored_documents = []

    for (
        document,
        semantic_score,
        store_type,
    ) in all_results:

        page_content = str(
            getattr(
                document,
                "page_content",
                "",
            )
            or ""
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

        # ----------------------------------------------------
        # SCORE NORMALIZATION
        # ----------------------------------------------------

        semantic_score = max(
            0.0,
            min(
                1.0,
                float(
                    semantic_score
                ),
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

        metadata = getattr(
            document,
            "metadata",
            {},
        )

        if not isinstance(
            metadata,
            dict,
        ):
            metadata = {}

        # ----------------------------------------------------
        # FORCE CORRECT SOURCE TYPE
        # ----------------------------------------------------

        if store_type == "conversation_file":

            metadata[
                "source_type"
            ] = "conversation_file"

        else:

            metadata.setdefault(
                "source_type",
                "global_knowledge",
            )

        # ----------------------------------------------------
        # STORE DEBUG SCORES
        # ----------------------------------------------------

        metadata[
            "semantic_score"
        ] = round(
            semantic_score,
            4,
        )

        metadata[
            "lexical_score"
        ] = round(
            lexical_score,
            4,
        )

        metadata[
            "phrase_score"
        ] = round(
            phrase_score,
            4,
        )

        metadata[
            "intent_score"
        ] = round(
            intent_score,
            4,
        )

        metadata[
            "relevance_score"
        ] = round(
            relevance_score,
            4,
        )

        metadata[
            "retrieval_source"
        ] = store_type

        document.metadata = metadata

        scored_documents.append(
            (
                document,
                semantic_score,
                lexical_score,
                phrase_score,
                intent_score,
                relevance_score,
                store_type,
            )
        )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique_documents = {}

    for item in scored_documents:

        document = item[0]

        identity = (
            document_identity(
                document
            )
        )

        existing = (
            unique_documents.get(
                identity
            )
        )

        if (
            existing is None
            or item[5] > existing[5]
        ):

            unique_documents[
                identity
            ] = item

    scored_documents = list(
        unique_documents.values()
    )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    scored_documents.sort(
        key=lambda item: item[5],
        reverse=True,
    )

    # --------------------------------------------------------
    # LOG TOP RESULTS
    # --------------------------------------------------------

    for rank, item in enumerate(
        scored_documents[:MAX_SOURCES],
        start=1,
    ):

        (
            document,
            semantic_score,
            lexical_score,
            phrase_score,
            intent_score,
            relevance_score,
            store_type,
        ) = item

        logger.info(
            "Candidate #%d | source=%s | "
            "semantic=%.4f | lexical=%.4f | "
            "phrase=%.4f | intent=%.4f | "
            "relevance=%.4f",
            rank,
            store_type,
            semantic_score,
            lexical_score,
            phrase_score,
            intent_score,
            relevance_score,
        )

    # --------------------------------------------------------
    # SELECT SOURCES
    # --------------------------------------------------------

    selected_documents = []

    if scored_documents:

        best_item = (
            scored_documents[0]
        )

        best_document = (
            best_item[0]
        )

        best_relevance = (
            best_item[5]
        )

        # ----------------------------------------------------
        # BEST RESULT
        # ----------------------------------------------------

        if (
            best_relevance
            >= MIN_BEST_RELEVANCE
        ):

            selected_documents.append(
                best_document
            )

            # ------------------------------------------------
            # ADDITIONAL SOURCES
            # ------------------------------------------------

            for item in scored_documents[1:]:

                if (
                    len(
                        selected_documents
                    )
                    >= MAX_SOURCES
                ):
                    break

                document = item[0]

                relevance_score = (
                    item[5]
                )

                if (
                    relevance_score
                    >= MIN_ADDITIONAL_RELEVANCE
                    and
                    relevance_score
                    >= (
                        best_relevance
                        * ADDITIONAL_SOURCE_RATIO
                    )
                ):

                    selected_documents.append(
                        document
                    )

    logger.info(
        "Retrieved %d total candidates; "
        "selected %d sources",
        len(scored_documents),
        len(selected_documents),
    )

    return selected_documents


# ============================================================
# PROMPT
# ============================================================

def build_prompt():

    return ChatPromptTemplate.from_template(
        """
You are a professional AI customer support assistant.

You answer questions using trusted information retrieved
from the available knowledge sources.

There are two possible factual sources:

1. Global Knowledge Base
2. Files attached to the current conversation

The retrieved context is the ONLY source of factual
information.

Previous conversation may be used only to understand
what the user is referring to. Do NOT use previous
conversation as a factual source.

If the answer is present in the retrieved context,
answer clearly and naturally.

If the user asks what is present in an attached file,
summarize the contents of the retrieved file context
rather than saying that the information is unavailable.

If the requested information is NOT present in the
retrieved context, say exactly:

"I don't know based on the available information."

Do not invent information.

Do not mention retrieval, embeddings, FAISS, vector
databases, chunks, semantic scores, or internal system
details unless the user explicitly asks about the
technical architecture.

Previous conversation:
{history}

Retrieved knowledge:
{context}

Current question:
{question}
"""
    )


# ============================================================
# PREPARE QA
# ============================================================

def prepare_qa(
    question,
    chat_history=None,
    chat_id=None,
):
    question = str(
        question or ""
    ).strip()

    if not question:

        raise ValueError(
            "Question cannot be empty."
        )

    chat_history = (
        chat_history or []
    )

    history_messages = (
        chat_history[-6:]
    )

    history_text = "\n".join(
        f"{message.get('role', '').capitalize()}: "
        f"{message.get('content', '')}"
        for message in history_messages
        if message.get(
            "content"
        )
    )

    documents = retrieve_documents(
        question,
        chat_history,
        chat_id,
    )

    if not documents:

        return {
            "messages": None,
            "source_documents": [],
            "has_context": False,
        }

    context_parts = []

    for document in documents:

        source_type = (
            document
            .metadata
            .get(
                "source_type",
                "global_knowledge",
            )
        )

        source_file = (
            document
            .metadata
            .get(
                "source_file",
                "",
            )
        )

        location = (
            document
            .metadata
            .get(
                "location",
                "",
            )
        )

        header = ""

        if source_type == "conversation_file":

            header = (
                f"Source: Conversation file\n"
                f"File: {source_file}\n"
                f"Location: {location}\n"
            )

        else:

            header = (
                "Source: Global Knowledge Base\n"
            )

        context_parts.append(
            header
            + "\n"
            + document.page_content
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    prompt = build_prompt()

    messages = prompt.invoke(
        {
            "history": (
                history_text
                or
                "No previous conversation."
            ),
            "context": context,
            "question": question,
        }
    )

    return {
        "messages": messages,
        "source_documents": documents,
        "has_context": True,
    }


# ============================================================
# RESPONSE TEXT EXTRACTION
# ============================================================

def extract_response_text(
    response,
):
    content = getattr(
        response,
        "content",
        response,
    )

    if isinstance(
        content,
        str,
    ):

        return content.strip()

    if isinstance(
        content,
        list,
    ):

        parts = []

        for item in content:

            if isinstance(
                item,
                str,
            ):

                parts.append(
                    item
                )

            elif isinstance(
                item,
                dict,
            ):

                text = item.get(
                    "text"
                )

                if text:
                    parts.append(
                        str(text)
                    )

        return "".join(
            parts
        ).strip()

    return str(
        content
    ).strip()


# ============================================================
# STREAM CHUNK EXTRACTION
# ============================================================

def extract_stream_text(
    chunk,
):
    content = getattr(
        chunk,
        "content",
        chunk,
    )

    if isinstance(
        content,
        str,
    ):

        return content

    if isinstance(
        content,
        list,
    ):

        parts = []

        for item in content:

            if isinstance(
                item,
                str,
            ):

                parts.append(
                    item
                )

            elif isinstance(
                item,
                dict,
            ):

                text = item.get(
                    "text"
                )

                if text:
                    parts.append(
                        str(text)
                    )

        return "".join(
            parts
        )

    return str(
        content or ""
    )


# ============================================================
# QA CHAIN
# ============================================================

def get_qa_chain():

    def ask_question(
        question,
        chat_history=None,
        chat_id=None,
    ):

        prepared = prepare_qa(
            question,
            chat_history,
            chat_id,
        )

        if not prepared[
            "has_context"
        ]:

            return {
                "result":
                    "I don't know based on the available information.",
                "source_documents": [],
            }

        response = (
            get_llm()
            .invoke(
                prepared[
                    "messages"
                ]
            )
        )

        answer = (
            extract_response_text(
                response
            )
        )

        return {
            "result": answer,
            "source_documents":
                prepared[
                    "source_documents"
                ],
        }

    return ask_question


# ============================================================
# STREAMING QA
# ============================================================

def get_qa_stream(
    question,
    chat_history=None,
    chat_id=None,
):
    """
    Returns:

        stream_generator,
        source_documents
    """

    prepared = prepare_qa(
        question,
        chat_history,
        chat_id,
    )

    if not prepared[
        "has_context"
    ]:

        def no_context_stream():

            yield (
                "I don't know based on "
                "the available information."
            )

        return (
            no_context_stream(),
            [],
        )

    messages = prepared[
        "messages"
    ]

    source_documents = prepared[
        "source_documents"
    ]

    def response_stream():

        for chunk in (
            get_llm()
            .stream(
                messages
            )
        ):

            text = extract_stream_text(
                chunk
            )

            if text:
                yield text

    return (
        response_stream(),
        source_documents,
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    logger.info("=" * 60)

    logger.info(
        "Customer Service Chatbot - Retrieval Test"
    )

    logger.info("=" * 60)

    create_vector_db()

    chain = get_qa_chain()

    test_question = (
        "What should I do if the device "
        "won't turn on?"
    )

    result = chain(
        test_question
    )

    logger.info(
        "Question: %s",
        test_question,
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