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

from config import (
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

logger.info(
    "Dataset path: %s",
    DATASET_PATH,
)

logger.info(
    "Vector DB path: %s",
    VECTORDB_PATH,
)


# ============================================================================
# GEMINI
# ============================================================================

@lru_cache(maxsize=1)
def get_llm():
    """Create and cache the Gemini language model."""

    logger.info(
        "Initializing Google Gemini LLM..."
    )

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


# ============================================================================
# EMBEDDINGS
# ============================================================================

@lru_cache(maxsize=1)
def get_embeddings():
    """Create and cache the HuggingFace embedding model."""

    logger.info(
        "Loading HuggingFace embeddings model..."
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG["model_name"]
    )

    logger.info(
        "Embeddings model loaded"
    )

    return embeddings


# ============================================================================
# CREATE VECTOR DATABASE
# ============================================================================

def create_vector_db():
    """Create a FAISS vector database from the CSV dataset."""

    logger.info("=" * 60)
    logger.info(
        "Starting vector database creation"
    )
    logger.info("=" * 60)

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}"
        )

    logger.info(
        "Loading dataset from: %s",
        DATASET_PATH,
    )

    loader = CSVLoader(
        file_path=str(DATASET_PATH),
        source_column=DATASET_CONFIG["csv_column"],
    )

    documents = loader.load()

    logger.info(
        "Loaded %d documents from CSV",
        len(documents),
    )

    embeddings = get_embeddings()

    logger.info(
        "Creating FAISS vector database..."
    )

    vectordb = FAISS.from_documents(
        documents,
        embeddings,
    )

    logger.info(
        "FAISS index created with %d vectors",
        vectordb.index.ntotal,
    )

    logger.info(
        "Saving FAISS index to: %s",
        VECTORDB_PATH,
    )

    vectordb.save_local(
        str(VECTORDB_PATH)
    )

    logger.info(
        "FAISS index saved successfully"
    )

    load_vector_db.cache_clear()

    logger.info(
        "Vector DB cache cleared"
    )

    logger.info(
        "Vector database creation completed"
    )

    return vectordb


# ============================================================================
# LOAD VECTOR DATABASE
# ============================================================================

@lru_cache(maxsize=1)
def load_vector_db():
    """Load and cache the FAISS vector database."""

    logger.info(
        "Loading FAISS vector database..."
    )

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


# ============================================================================
# PROMPT
# ============================================================================

def get_prompt():
    """Return the RAG prompt."""

    return ChatPromptTemplate.from_template(
        """
You are a helpful customer service assistant.

Your job is to answer the user's question using ONLY
the information provided in the knowledge-base context.

You may use the previous conversation to understand
what the user is referring to.

IMPORTANT RULES:

1. The knowledge-base context is the only source of facts.
2. Previous conversation is only for understanding context.
3. Do not use previous conversation as a factual source.
4. Do not make up information.
5. Do not assume information that is not present.
6. If the answer is not present in the knowledge-base context,
   say exactly:

"I don't know based on the available information."

7. Keep the answer clear and helpful.
8. If the user asks a follow-up question, use the conversation
   to understand what they mean, but verify the answer from
   the knowledge base.

Previous conversation:
{history}

Knowledge-base context:
{context}

Current question:
{question}
"""
    )


# ============================================================================
# HISTORY
# ============================================================================

def build_history(chat_history):
    """Convert chat history into readable text."""

    if not chat_history:
        return "No previous conversation."

    history_messages = chat_history[-6:]

    history_text = "\n".join(
        f"{message['role'].capitalize()}: "
        f"{message['content']}"
        for message in history_messages
        if message.get("content")
    )

    return (
        history_text
        if history_text
        else "No previous conversation."
    )


# ============================================================================
# RETRIEVAL
# ============================================================================

def retrieve_documents(
    retriever,
    question,
    chat_history=None,
):
    """Retrieve relevant documents."""

    history_text = build_history(
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
        "Retrieval query: %s",
        question[:80],
    )

    documents = retriever.invoke(
        retrieval_query
    )

    logger.info(
        "Retrieved %d documents",
        len(documents),
    )

    return documents, history_text


# ============================================================================
# RESPONSE CONVERSION
# ============================================================================

def extract_text(content):
    """Convert Gemini response content into plain text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):

                text_parts.append(item)

            elif (
                isinstance(item, dict)
                and "text" in item
            ):

                text_parts.append(
                    item["text"]
                )

        return "".join(text_parts)

    return str(content)


# ============================================================================
# QA CHAIN
# ============================================================================

def get_qa_chain():
    """Create the standard RAG question-answering function."""

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": RETRIEVER_CONFIG["k"],
        }
    )

    prompt = get_prompt()

    logger.info(
        "QA chain ready with retriever k=%d",
        RETRIEVER_CONFIG["k"],
    )

    def ask_question(
        question,
        chat_history=None,
    ):
        """Answer a question using RAG."""

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        documents, history_text = (
            retrieve_documents(
                retriever,
                question,
                chat_history,
            )
        )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        logger.info(
            "Context size: %d characters",
            len(context),
        )

        messages = prompt.invoke(
            {
                "history": history_text,
                "context": context,
                "question": question,
            }
        )

        logger.info(
            "Generating response with Gemini..."
        )

        response = get_llm().invoke(
            messages
        )

        answer = extract_text(
            response.content
        ).strip()

        logger.info(
            "Answer generated: %d characters",
            len(answer),
        )

        return {
            "result": answer,
            "source_documents": documents,
        }

    return ask_question


# ============================================================================
# STREAMING QA
# ============================================================================

def get_streaming_qa_chain():
    """Create a streaming RAG question-answering function."""

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": RETRIEVER_CONFIG["k"],
        }
    )

    prompt = get_prompt()

    logger.info(
        "Streaming QA chain ready"
    )

    def stream_question(
        question,
        chat_history=None,
    ):
        """Stream an answer using RAG."""

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        documents, history_text = (
            retrieve_documents(
                retriever,
                question,
                chat_history,
            )
        )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        logger.info(
            "Streaming context size: %d characters",
            len(context),
        )

        messages = prompt.invoke(
            {
                "history": history_text,
                "context": context,
                "question": question,
            }
        )

        logger.info(
            "Starting Gemini streaming response..."
        )

        yield {
            "type": "sources",
            "source_documents": documents,
        }

        for chunk in get_llm().stream(
            messages
        ):

            text = extract_text(
                chunk.content
            )

            if text:

                yield {
                    "type": "token",
                    "content": text,
                }

        logger.info(
            "Streaming response completed"
        )

    return stream_question


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info(
        "TESTING QA CHAIN"
    )
    logger.info("=" * 60)

    try:

        logger.info(
            "Step 1: Creating vector database"
        )

        create_vector_db()

        logger.info(
            "Step 2: Creating QA chain"
        )

        chain = get_qa_chain()

        logger.info(
            "Step 3: Testing sample question"
        )

        test_question = (
            "Do you provide internships?"
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
            "Sources: %d",
            len(
                result["source_documents"]
            ),
        )

        logger.info("=" * 60)
        logger.info(
            "TEST PASSED"
        )
        logger.info("=" * 60)

    except Exception as error:

        logger.error(
            "TEST FAILED: %s",
            error,
            exc_info=True,
        )