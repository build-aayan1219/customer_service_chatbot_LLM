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


os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "dataset.csv"
VECTORDB_PATH = BASE_DIR / "faiss_index"
LOG_FILE_PATH = BASE_DIR / LOGGING_CONFIG["log_file"]


logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
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

logger.info("Dataset path: %s", DATASET_PATH)
logger.info("Vector DB path: %s", VECTORDB_PATH)


@lru_cache(maxsize=1)
def get_llm():
    """Create and cache the Gemini language model."""

    logger.info("Initializing Google Gemini LLM...")

    api_key = os.getenv("GOOGLE_API_KEY")

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

    logger.info("Gemini LLM initialized")

    return llm


@lru_cache(maxsize=1)
def get_embeddings():
    """Create and cache the HuggingFace embedding model."""

    logger.info("Loading HuggingFace embeddings model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG["model_name"]
    )

    logger.info("Embeddings model loaded")

    return embeddings


def create_vector_db():
    """Create a FAISS vector database from the CSV dataset."""

    logger.info("=" * 60)
    logger.info("Starting vector database creation")
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

    logger.info("Creating FAISS vector database...")

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

    vectordb.save_local(str(VECTORDB_PATH))

    logger.info("FAISS index saved successfully")

    load_vector_db.cache_clear()

    logger.info("Vector DB cache cleared")
    logger.info("Vector database creation completed")

    return vectordb


@lru_cache(maxsize=1)
def load_vector_db():
    """Load and cache the FAISS vector database."""

    logger.info("Loading FAISS vector database...")

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


def get_qa_chain():
    """Create the RAG question-answering functions."""

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": RETRIEVER_CONFIG["k"],
        }
    )

    logger.info(
        "QA chain ready with retriever k=%d",
        RETRIEVER_CONFIG["k"],
    )

    prompt = ChatPromptTemplate.from_template(
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

Previous conversation:
{history}

Knowledge-base context:
{context}

Current question:
{question}
"""
    )

    def prepare_request(question, chat_history=None):
        """Prepare the RAG prompt and retrieved documents."""

        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        chat_history = chat_history or []

        history_messages = chat_history[-6:]

        history_text = "\n".join(
            f"{message['role'].capitalize()}: "
            f"{message['content']}"
            for message in history_messages
            if message.get("content")
        )

        retrieval_query = question

        if history_text:
            retrieval_query = (
                "Previous conversation:\n"
                f"{history_text}\n\n"
                "Current question:\n"
                f"{question}"
            )

        logger.info(
            "Processing question: %s",
            question[:80],
        )

        documents = retriever.invoke(
            retrieval_query
        )

        logger.info(
            "Retrieved %d documents",
            len(documents),
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
                "history": (
                    history_text
                    if history_text
                    else "No previous conversation."
                ),
                "context": context,
                "question": question,
            }
        )

        return messages, documents

    def ask_question(question, chat_history=None):
        """Answer a question using normal non-streaming RAG."""

        messages, documents = prepare_request(
            question,
            chat_history,
        )

        logger.info(
            "Generating response with Gemini..."
        )

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
            "Answer generated: %d characters",
            len(answer),
        )

        return {
            "result": answer,
            "source_documents": documents,
        }

    def ask_question_stream(question, chat_history=None):
        """Stream a RAG response from Gemini."""

        messages, documents = prepare_request(
            question,
            chat_history,
        )

        logger.info(
            "Starting streaming response with Gemini..."
        )

        for chunk in get_llm().stream(messages):

            content = chunk.content

            if isinstance(content, str):

                if content:
                    yield {
                        "type": "token",
                        "content": content,
                    }

            elif isinstance(content, list):

                for item in content:

                    if isinstance(item, dict):

                        text = item.get("text", "")

                        if text:
                            yield {
                                "type": "token",
                                "content": text,
                            }

        logger.info("Streaming response completed")

        yield {
            "type": "sources",
            "source_documents": documents,
        }

    return ask_question, ask_question_stream


if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info("TESTING QA CHAIN")
    logger.info("=" * 60)

    try:

        logger.info(
            "Step 1: Creating vector database"
        )

        create_vector_db()

        logger.info(
            "Step 2: Creating QA chain"
        )

        chain, stream_chain = get_qa_chain()

        logger.info(
            "Step 3: Testing sample question"
        )

        test_question = "Do you provide internships?"

        result = chain(test_question)

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
            len(result["source_documents"]),
        )

        logger.info("=" * 60)
        logger.info("TEST PASSED")
        logger.info("=" * 60)

    except Exception as error:

        logger.error(
            "TEST FAILED: %s",
            error,
            exc_info=True,
        )