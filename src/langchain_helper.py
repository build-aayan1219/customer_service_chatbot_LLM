import logging
import os
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


# ============================================================================
# ENVIRONMENT
# ============================================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


# ============================================================================
# PATHS
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "dataset.csv"
VECTORDB_PATH = BASE_DIR / "faiss_index"
LOG_FILE_PATH = BASE_DIR / LOGGING_CONFIG["log_file"]


# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(
            LOG_FILE_PATH,
            encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

logger.info("Dataset path: %s", DATASET_PATH)
logger.info("Vector DB path: %s", VECTORDB_PATH)


# ============================================================================
# GEMINI
# ============================================================================

@lru_cache(maxsize=1)
def get_llm():
    """Create and cache the Gemini LLM."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Add it to the .env file or Streamlit secrets."
        )

    logger.info("Initializing Google Gemini LLM...")

    llm = ChatGoogleGenerativeAI(
        model=LLM_CONFIG["model"],
        google_api_key=api_key,
        temperature=LLM_CONFIG["temperature"],
        max_tokens=LLM_CONFIG["max_tokens"],
    )

    logger.info("Gemini LLM initialized")

    return llm


# ============================================================================
# EMBEDDINGS
# ============================================================================

@lru_cache(maxsize=1)
def get_embeddings():
    """Create and cache the HuggingFace embeddings model."""

    logger.info("Loading HuggingFace embeddings model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG["model_name"]
    )

    logger.info("Embeddings model loaded")

    return embeddings


# ============================================================================
# CREATE VECTOR DATABASE
# ============================================================================

def create_vector_db():
    """Create a FAISS vector database from the CSV dataset."""

    try:
        logger.info("=" * 60)
        logger.info("Starting vector database creation")
        logger.info("=" * 60)

        if not DATASET_PATH.exists():
            raise FileNotFoundError(
                f"Dataset not found at: {DATASET_PATH}"
            )

        logger.info("Loading dataset from: %s", DATASET_PATH)

        loader = CSVLoader(
            file_path=str(DATASET_PATH),
            source_column=DATASET_CONFIG["csv_column"],
        )

        documents = loader.load()

        if not documents:
            raise ValueError("The dataset contains no documents.")

        logger.info(
            "Loaded %s documents from CSV",
            len(documents),
        )

        embeddings = get_embeddings()

        logger.info("Creating FAISS vector database...")

        vectordb = FAISS.from_documents(
            documents,
            embeddings,
        )

        logger.info(
            "FAISS index created with %s vectors",
            vectordb.index.ntotal,
        )

        VECTORDB_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Saving FAISS index to: %s",
            VECTORDB_PATH,
        )

        vectordb.save_local(str(VECTORDB_PATH))

        logger.info("FAISS index saved successfully")

        load_vector_db.cache_clear()

        logger.info("Vector DB cache cleared")
        logger.info("Vector database creation completed")
        logger.info("=" * 60)

        return vectordb

    except Exception as e:
        logger.error(
            "Error creating vector database: %s",
            e,
            exc_info=True,
        )
        raise


# ============================================================================
# LOAD VECTOR DATABASE
# ============================================================================

@lru_cache(maxsize=1)
def load_vector_db():
    """Load and cache the FAISS vector database."""

    logger.info("Loading FAISS vector database...")

    if not VECTORDB_PATH.exists():
        raise FileNotFoundError(
            f"Vector database not found at: {VECTORDB_PATH}. "
            "Please create it first."
        )

    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    logger.info(
        "Loaded FAISS index with %s vectors",
        vectordb.index.ntotal,
    )

    return vectordb


# ============================================================================
# QA CHAIN
# ============================================================================

def get_qa_chain():
    """Create the RAG question-answering function."""

    try:
        logger.info("Creating QA chain...")

        vectordb = load_vector_db()

        retriever = vectordb.as_retriever(
            search_kwargs={
                "k": RETRIEVER_CONFIG["k"]
            }
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are a helpful customer service assistant.

Answer the question using ONLY the information provided in the context.

If the answer is not present in the context, say:
"I don't know based on the available information."

Do not make up information.

Context:
{context}

Question:
{question}
"""
        )

        logger.info(
            "QA chain ready with retriever k=%s",
            RETRIEVER_CONFIG["k"],
        )

        def ask_question(question: str):
            """Answer a question using the RAG pipeline."""

            if not question or not question.strip():
                raise ValueError("Question cannot be empty.")

            question = question.strip()

            logger.info(
                "Processing question: %s",
                question[:60],
            )

            documents = retriever.invoke(question)

            logger.info(
                "Retrieved %s documents",
                len(documents),
            )

            context = "\n\n".join(
                document.page_content
                for document in documents
            )

            logger.info(
                "Context size: %s characters",
                len(context),
            )

            messages = prompt.invoke(
                {
                    "context": context,
                    "question": question,
                }
            )

            logger.info("Generating response with Gemini...")

            response = get_llm().invoke(messages)

            answer = response.content

            if isinstance(answer, list):
                text_parts = []

                for item in answer:
                    if isinstance(item, dict) and "text" in item:
                        text_parts.append(item["text"])

                answer = "".join(text_parts)

            answer = str(answer).strip()

            logger.info(
                "Answer generated: %s characters",
                len(answer),
            )

            return {
                "result": answer,
                "source_documents": documents,
            }

        return ask_question

    except Exception as e:
        logger.error(
            "Error creating QA chain: %s",
            e,
            exc_info=True,
        )
        raise


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info("TESTING QA CHAIN")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: Creating vector database")

        create_vector_db()

        logger.info("Step 2: Creating QA chain")

        chain = get_qa_chain()

        logger.info("Step 3: Testing sample question")

        test_question = "Do you provide internships?"

        result = chain(test_question)

        logger.info("Question: %s", test_question)
        logger.info("Answer: %s", result["result"])
        logger.info(
            "Sources: %s",
            len(result["source_documents"]),
        )

        logger.info("=" * 60)
        logger.info("TEST PASSED")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(
            "TEST FAILED: %s",
            e,
            exc_info=True,
        )