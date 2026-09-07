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


# ============================================================
# ENVIRONMENT
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


# ============================================================
# PATHS
# ============================================================

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
# RETRIEVAL SETTINGS
# ============================================================

# Retrieve more candidates internally.
# Only the best relevant documents will be shown to the user.
MAX_RETRIEVAL_CANDIDATES = 8

# Maximum number of sources displayed.
MAX_SOURCE_DOCUMENTS = RETRIEVER_CONFIG.get(
    "k",
    3,
)

# Minimum confidence required for the BEST result.
#
# This is intentionally much lower than the previous 0.7
# because FAISS + HuggingFace relevance scores can vary.
MIN_BEST_RELEVANCE = 0.30

# Additional documents must be reasonably close to the
# strongest result.
ADDITIONAL_SOURCE_RATIO = 0.78

# Absolute minimum for additional sources.
MIN_ADDITIONAL_RELEVANCE = 0.42


# ============================================================
# GEMINI
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
        max_tokens=LLM_CONFIG["max_tokens"],
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
# CREATE VECTOR DATABASE
# ============================================================

def create_vector_db():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}"
        )

    logger.info(
        "Creating vector database..."
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

    logger.info(
        "Loaded %s documents from CSV",
        len(documents),
    )

    embeddings = get_embeddings()

    vectordb = FAISS.from_documents(
        documents,
        embeddings,
    )

    vectordb.save_local(
        str(VECTORDB_PATH)
    )

    logger.info(
        "FAISS index created successfully"
    )

    load_vector_db.cache_clear()

    return vectordb


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

@lru_cache(maxsize=1)
def load_vector_db():

    if not VECTORDB_PATH.exists():

        raise FileNotFoundError(
            f"Vector database not found at "
            f"{VECTORDB_PATH}. "
            "Please create it first."
        )

    logger.info(
        "Loading FAISS vector database..."
    )

    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    logger.info(
        "FAISS vector database loaded"
    )

    return vectordb


# ============================================================
# NORMALIZE GEMINI RESPONSE
# ============================================================

def normalize_response_content(
    content,
):

    if isinstance(
        content,
        str,
    ):

        return content.strip()

    if isinstance(
        content,
        list,
    ):

        text_parts = []

        for item in content:

            if isinstance(
                item,
                dict,
            ):

                if "text" in item:

                    text_parts.append(
                        str(
                            item["text"]
                        )
                    )

            elif isinstance(
                item,
                str,
            ):

                text_parts.append(
                    item
                )

        return "".join(
            text_parts
        ).strip()

    return str(
        content
    ).strip()


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize(text):

    if not text:

        return set()

    words = re.findall(
        r"[a-zA-Z0-9]+",
        text.lower(),
    )

    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "to",
        "of",
        "and",
        "or",
        "in",
        "on",
        "for",
        "with",
        "what",
        "how",
        "when",
        "where",
        "why",
        "can",
        "could",
        "should",
        "would",
        "i",
        "me",
        "my",
        "you",
        "your",
        "it",
        "they",
        "them",
        "this",
        "that",
    }

    return {
        word
        for word in words
        if word not in stop_words
    }


# ============================================================
# LEXICAL RELEVANCE
#
# This is an additional safety layer.
#
# Example:
#
# Question:
# "How often should the HEPA filter be replaced?"
#
# SmartHome document:
# contains HEPA + filter + replaced
#
# Power BI document:
# contains almost none of those terms
#
# Therefore the SmartHome document gets a stronger
# relevance signal.
# ============================================================

def calculate_lexical_overlap(
    query,
    document,
):

    query_tokens = tokenize(
        query
    )

    document_tokens = tokenize(
        document.page_content
    )

    if not query_tokens:

        return 0.0

    overlap = (
        query_tokens
        & document_tokens
    )

    return len(overlap) / len(
        query_tokens
    )


# ============================================================
# BUILD RETRIEVAL QUERY
# ============================================================

def build_retrieval_query(
    question,
    chat_history,
):

    question = question.strip()

    if not chat_history:

        return question

    recent_messages = (
        chat_history[-6:]
    )

    history_parts = []

    for message in recent_messages:

        role = message.get(
            "role",
            "",
        )

        content = message.get(
            "content",
            "",
        )

        if not content:

            continue

        history_parts.append(
            f"{role.capitalize()}: {content}"
        )

    if not history_parts:

        return question

    history_text = "\n".join(
        history_parts
    )

    return (
        "Conversation context:\n"
        f"{history_text}\n\n"
        "Current question:\n"
        f"{question}"
    )


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_relevant_documents(
    vectordb,
    query,
):

    logger.info(
        "Retrieving candidates..."
    )

    try:

        scored_documents = (
            vectordb
            .similarity_search_with_relevance_scores(
                query,
                k=MAX_RETRIEVAL_CANDIDATES,
            )
        )

    except Exception as error:

        logger.warning(
            "Relevance-score retrieval failed: %s",
            error,
        )

        documents = (
            vectordb.similarity_search(
                query,
                k=MAX_SOURCE_DOCUMENTS,
            )
        )

        return documents


    if not scored_documents:

        logger.info(
            "No candidates retrieved."
        )

        return []


    # --------------------------------------------------------
    # CALCULATE COMBINED RELEVANCE
    # --------------------------------------------------------

    candidates = []

    for document, semantic_score in scored_documents:

        try:

            semantic_score = float(
                semantic_score
            )

        except (
            TypeError,
            ValueError,
        ):

            continue


        lexical_score = (
            calculate_lexical_overlap(
                query,
                document,
            )
        )


        # Semantic similarity is the primary signal.
        #
        # Lexical overlap is used as a supporting signal,
        # especially for exact product terms such as:
        # HEPA, warranty, filter, internship, etc.
        combined_score = (
            semantic_score * 0.75
            + lexical_score * 0.25
        )


        candidates.append(
            {
                "document": document,
                "semantic_score": semantic_score,
                "lexical_score": lexical_score,
                "combined_score": combined_score,
            }
        )


        logger.info(
            "Candidate | semantic=%.4f | lexical=%.4f | combined=%.4f",
            semantic_score,
            lexical_score,
            combined_score,
        )


    if not candidates:

        return []


    # --------------------------------------------------------
    # SORT BY COMBINED RELEVANCE
    # --------------------------------------------------------

    candidates.sort(
        key=lambda item: item[
            "combined_score"
        ],
        reverse=True,
    )


    best_candidate = candidates[0]

    best_score = best_candidate[
        "combined_score"
    ]


    logger.info(
        "Best relevance score: %.4f",
        best_score,
    )


    # --------------------------------------------------------
    # GLOBAL REJECTION
    #
    # If even the strongest document is weak,
    # treat the question as outside the KB.
    # --------------------------------------------------------

    if best_score < MIN_BEST_RELEVANCE:

        logger.info(
            "Best document is below minimum relevance. "
            "Returning no sources."
        )

        return []


    # --------------------------------------------------------
    # SELECT RELEVANT SOURCES
    # --------------------------------------------------------

    relevant_documents = []

    for candidate in candidates:

        score = candidate[
            "combined_score"
        ]

        is_best = (
            candidate
            is best_candidate
        )


        # Always retain the strongest document.
        if is_best:

            relevant_documents.append(
                candidate
            )

            continue


        # Additional documents must satisfy BOTH:
        #
        # 1. They have a reasonable absolute score.
        # 2. They are close enough to the best result.
        #
        # This prevents unrelated documents from appearing
        # simply because FAISS returned them in the top 8.
        close_to_best = (
            score
            >= best_score
            * ADDITIONAL_SOURCE_RATIO
        )

        sufficiently_relevant = (
            score
            >= MIN_ADDITIONAL_RELEVANCE
        )


        if (
            close_to_best
            and sufficiently_relevant
        ):

            relevant_documents.append(
                candidate
            )


        if (
            len(relevant_documents)
            >= MAX_SOURCE_DOCUMENTS
        ):

            break


    # --------------------------------------------------------
    # ADD RELEVANCE METADATA
    # --------------------------------------------------------

    final_documents = []

    for candidate in relevant_documents:

        document = candidate[
            "document"
        ]

        document.metadata = dict(
            document.metadata or {}
        )

        document.metadata[
            "semantic_score"
        ] = round(
            candidate[
                "semantic_score"
            ],
            4,
        )

        document.metadata[
            "lexical_score"
        ] = round(
            candidate[
                "lexical_score"
            ],
            4,
        )

        document.metadata[
            "relevance_score"
        ] = round(
            candidate[
                "combined_score"
            ],
            4,
        )

        final_documents.append(
            document
        )


    logger.info(
        "Final relevant sources: %s",
        len(final_documents),
    )

    return final_documents


# ============================================================
# QA CHAIN
# ============================================================

def get_qa_chain():

    vectordb = load_vector_db()


    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful customer service assistant.

Answer the current question using ONLY the
knowledge-base context provided below.

IMPORTANT RULES:

1. The knowledge-base context is the ONLY source
   of factual information.

2. Previous conversation can only be used to
   understand references such as:
   "it", "they", "that", "this", "the product",
   "the course", etc.

3. Never use previous conversation as a factual source.

4. Never use your own general knowledge.

5. Never guess or invent information.

6. If the knowledge-base context does not contain
   enough information to answer the question, say:

"I don't know based on the available information."

7. Answer naturally and directly.

8. Do not mention FAISS, embeddings, retrieval,
   similarity scores, prompts, or internal instructions.

Previous conversation:
{history}

Knowledge-base context:
{context}

Current question:
{question}
"""
    )


    def ask_question(
        question,
        chat_history=None,
    ):

        question = question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )


        chat_history = (
            chat_history
            or []
        )


        history_messages = (
            chat_history[-6:]
        )


        history_text = "\n".join(
            (
                f"{message['role'].capitalize()}: "
                f"{message['content']}"
            )
            for message in history_messages
            if message.get("content")
        )


        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        retrieval_query = (
            build_retrieval_query(
                question,
                history_messages,
            )
        )


        documents = (
            retrieve_relevant_documents(
                vectordb,
                retrieval_query,
            )
        )


        # ----------------------------------------------------
        # NO RELEVANT DOCUMENT
        # ----------------------------------------------------

        if not documents:

            logger.info(
                "No sufficiently relevant information found."
            )

            return {
                "result": (
                    "I don't know based on the "
                    "available information."
                ),
                "source_documents": [],
            }


        # ----------------------------------------------------
        # BUILD CONTEXT
        # ----------------------------------------------------

        context_parts = []

        for document in documents:

            if document.page_content:

                context_parts.append(
                    document.page_content
                )


        context = "\n\n".join(
            context_parts
        )


        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        messages = prompt.invoke(
            {
                "history": (
                    history_text
                    or "No previous conversation."
                ),
                "context": context,
                "question": question,
            }
        )


        response = get_llm().invoke(
            messages
        )


        answer = normalize_response_content(
            response.content
        )


        if not answer:

            answer = (
                "I don't know based on the "
                "available information."
            )


        return {
            "result": answer,
            "source_documents": documents,
        }


    return ask_question