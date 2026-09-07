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
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


logger = logging.getLogger(__name__)


# Retrieval tuning
MAX_RETRIEVAL_CANDIDATES = 8
MIN_BEST_RELEVANCE = 0.30

# A secondary source must be close to the best source and also
# independently relevant. This prevents weakly related chunks
# from appearing in the Sources section.
ADDITIONAL_SOURCE_RATIO = 0.88
MIN_ADDITIONAL_RELEVANCE = 0.46
MAX_SOURCES = 3


def normalize_text(text):
    """Normalize text for lexical comparison."""
    return re.findall(r"\b[a-z0-9]+\b", str(text).lower())


def calculate_lexical_overlap(query, document_text):
    """Calculate the proportion of query terms found in a document."""
    query_terms = set(normalize_text(query))
    document_terms = set(normalize_text(document_text))

    if not query_terms:
        return 0.0

    return len(query_terms.intersection(document_terms)) / len(query_terms)


def calculate_combined_relevance(semantic_score, lexical_score):
    """
    Combine semantic and lexical relevance.

    Semantic similarity remains the primary signal while lexical
    overlap helps distinguish closely related support sections.
    """
    return (semantic_score * 0.75) + (lexical_score * 0.25)


@lru_cache(maxsize=1)
def get_llm():
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
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_CONFIG["model_name"]
    )

    logger.info("Embeddings model loaded")
    return embeddings


def create_vector_db():
    """Create and save the FAISS vector database from the current dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}"
        )

    loader = CSVLoader(
        file_path=str(DATASET_PATH),
        source_column=DATASET_CONFIG["csv_column"],
    )

    documents = loader.load()

    if not documents:
        raise ValueError("The dataset does not contain any documents.")

    embeddings = get_embeddings()

    vectordb = FAISS.from_documents(
        documents,
        embeddings,
    )

    VECTORDB_PATH.mkdir(parents=True, exist_ok=True)

    vectordb.save_local(str(VECTORDB_PATH))

    load_vector_db.cache_clear()

    logger.info(
        "FAISS vector database created with %d documents",
        len(documents),
    )

    return vectordb


@lru_cache(maxsize=1)
def load_vector_db():
    """Load the existing FAISS vector database."""
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


def _build_prompt():
    """Build the shared customer-service prompt."""
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

Previous conversation:
{history}

Knowledge-base context:
{context}

Current question:
{question}
"""
    )


def _prepare_qa(question, chat_history=None):
    """
    Retrieve relevant documents and prepare the prompt.

    This shared function is used by both normal and streaming
    responses so that retrieval behavior remains identical.
    """
    question = str(question).strip()

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

    logger.info("Question: %s", question)

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": MAX_RETRIEVAL_CANDIDATES,
        }
    )

    # Retrieve more candidates than we finally expose so that
    # relevance filtering has enough choices.
    candidate_documents = retriever.invoke(retrieval_query)

    scored_documents = []

    # similarity_search_with_relevance_scores gives normalized
    # relevance scores for the same FAISS store.
    try:
        scored_results = (
            vectordb.similarity_search_with_relevance_scores(
                retrieval_query,
                k=MAX_RETRIEVAL_CANDIDATES,
            )
        )
    except Exception:
        scored_results = []

    if scored_results:
        for document, semantic_score in scored_results:
            lexical_score = calculate_lexical_overlap(
                question,
                document.page_content,
            )

            relevance_score = calculate_combined_relevance(
                semantic_score,
                lexical_score,
            )

            document.metadata["semantic_score"] = round(
                float(semantic_score),
                4,
            )

            document.metadata["lexical_score"] = round(
                float(lexical_score),
                4,
            )

            document.metadata["relevance_score"] = round(
                float(relevance_score),
                4,
            )

            scored_documents.append(
                (
                    document,
                    float(semantic_score),
                    float(lexical_score),
                    float(relevance_score),
                )
            )

    # Fallback for vector-store implementations that do not return
    # normalized relevance scores.
    if not scored_documents:
        for rank, document in enumerate(candidate_documents):
            lexical_score = calculate_lexical_overlap(
                question,
                document.page_content,
            )

            # Preserve ordering when an explicit semantic score
            # cannot be obtained.
            semantic_score = max(
                0.0,
                1.0 - (rank / max(len(candidate_documents), 1)),
            )

            relevance_score = calculate_combined_relevance(
                semantic_score,
                lexical_score,
            )

            document.metadata["semantic_score"] = round(
                float(semantic_score),
                4,
            )

            document.metadata["lexical_score"] = round(
                float(lexical_score),
                4,
            )

            document.metadata["relevance_score"] = round(
                float(relevance_score),
                4,
            )

            scored_documents.append(
                (
                    document,
                    semantic_score,
                    lexical_score,
                    relevance_score,
                )
            )

    scored_documents.sort(
        key=lambda item: item[3],
        reverse=True,
    )

    selected_documents = []

    if scored_documents:
        best_document, _, _, best_relevance = scored_documents[0]

        # If the strongest result itself is too weak, do not let
        # unrelated content become the answer context.
        if best_relevance >= MIN_BEST_RELEVANCE:
            selected_documents.append(best_document)

            # Add secondary sources only when they are close to the
            # best result AND independently relevant.
            for (
                document,
                _semantic_score,
                _lexical_score,
                relevance_score,
            ) in scored_documents[1:]:
                if len(selected_documents) >= MAX_SOURCES:
                    break

                if (
                    relevance_score >= MIN_ADDITIONAL_RELEVANCE
                    and relevance_score
                    >= best_relevance * ADDITIONAL_SOURCE_RATIO
                ):
                    selected_documents.append(document)

    logger.info(
        "Retrieved %d candidates; selected %d relevant sources",
        len(scored_documents),
        len(selected_documents),
    )

    if not selected_documents:
        return {
            "question": question,
            "history": history_text or "No previous conversation.",
            "context": "",
            "messages": None,
            "source_documents": [],
            "no_answer": True,
        }

    context = "\n\n".join(
        document.page_content
        for document in selected_documents
    )

    logger.info(
        "Context size: %d characters",
        len(context),
    )

    prompt = _build_prompt()

    messages = prompt.invoke(
        {
            "history": history_text or "No previous conversation.",
            "context": context,
            "question": question,
        }
    )

    return {
        "question": question,
        "history": history_text or "No previous conversation.",
        "context": context,
        "messages": messages,
        "source_documents": selected_documents,
        "no_answer": False,
    }


def get_qa_chain():
    """
    Create the customer-service RAG question-answering function.

    Retrieval uses semantic similarity plus lexical overlap.
    The strongest relevant source is always retained. Additional
    sources are included only when they are sufficiently close to
    the strongest source and independently relevant.
    """

    def ask_question(question, chat_history=None):
        prepared = _prepare_qa(
            question,
            chat_history,
        )

        if prepared["no_answer"]:
            return {
                "result": "I don't know based on the available information.",
                "source_documents": [],
            }

        logger.info("Generating response with Gemini...")

        response = get_llm().invoke(
            prepared["messages"]
        )

        answer = response.content

        if isinstance(answer, list):
            text_parts = []

            for item in answer:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, str):
                    text_parts.append(item)

            answer = "".join(text_parts)

        answer = str(answer).strip()

        return {
            "result": answer,
            "source_documents": prepared["source_documents"],
        }

    return ask_question


def get_qa_stream(question, chat_history=None):
    """
    Prepare a streaming RAG response.

    Returns:
        stream_generator:
            Generator that yields Gemini response chunks.

        source_documents:
            The same selected documents used to generate the answer.

    The retrieval and relevance filtering are exactly the same as
    the normal get_qa_chain() implementation.
    """

    prepared = _prepare_qa(
        question,
        chat_history,
    )

    source_documents = prepared["source_documents"]

    if prepared["no_answer"]:

        def unknown_stream():
            yield "I don't know based on the available information."

        return unknown_stream(), source_documents

    logger.info("Starting streaming response with Gemini...")

    def response_stream():
        try:
            for chunk in get_llm().stream(
                prepared["messages"]
            ):
                content = getattr(
                    chunk,
                    "content",
                    "",
                )

                if isinstance(content, list):
                    text_parts = []

                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(item["text"])
                        elif isinstance(item, str):
                            text_parts.append(item)

                    content = "".join(text_parts)

                if content:
                    yield str(content)

        except Exception:
            logger.exception(
                "Error while streaming Gemini response"
            )
            raise

    return response_stream(), source_documents


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Customer Service Chatbot - Vector Database Test")
    logger.info("=" * 60)

    create_vector_db()

    chain = get_qa_chain()

    test_question = "What should I do if the device won't turn on?"

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
        "Selected sources: %d",
        len(result["source_documents"]),
    )

    logger.info("=" * 60)
    logger.info("Testing streaming response...")
    logger.info("=" * 60)

    stream, sources = get_qa_stream(test_question)

    streamed_answer = ""

    for chunk in stream:
        print(chunk, end="", flush=True)
        streamed_answer += chunk

    print()

    logger.info(
        "Streaming answer completed with %d sources",
        len(sources),
    )