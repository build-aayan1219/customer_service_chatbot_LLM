import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""

from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate


# ---------------- ENVIRONMENT ----------------

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "dataset.csv"
VECTORDB_PATH = BASE_DIR / "faiss_index"


# ---------------- GEMINI ----------------

@lru_cache(maxsize=1)
def get_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )


# ---------------- EMBEDDINGS ----------------

@lru_cache(maxsize=1)
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ---------------- CREATE KNOWLEDGE BASE ----------------

def create_vector_db():

    loader = CSVLoader(
        file_path=str(DATASET_PATH),
        source_column="prompt"
    )

    data = loader.load()

    vectordb = FAISS.from_documents(
        data,
        get_embeddings()
    )

    vectordb.save_local(str(VECTORDB_PATH))

    # Clear old cached database
    load_vector_db.cache_clear()

    return vectordb


# ---------------- LOAD FAISS DATABASE ----------------

@lru_cache(maxsize=1)
def load_vector_db():

    return FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True
    )


# ---------------- QA CHAIN ----------------

def get_qa_chain():

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 3}
    )

    prompt = ChatPromptTemplate.from_template("""
You are a helpful customer service assistant.

Answer the question using ONLY the information provided in the context.

If the answer is not present in the context, say:
"I don't know based on the available information."

Do not make up information.

Context:
{context}

Question:
{question}
""")

    def ask_question(question):

        documents = retriever.invoke(question)

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        messages = prompt.invoke({
            "context": context,
            "question": question
        })

        response = get_llm().invoke(messages)

        # Extract only actual text
        answer = response.content

        if isinstance(answer, list):

            text_parts = []

            for item in answer:

                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])

            answer = "".join(text_parts)

        answer = str(answer).strip()

        return {
            "result": answer,
            "source_documents": documents
        }

    return ask_question


# ---------------- TEST ----------------

if __name__ == "__main__":

    create_vector_db()

    chain = get_qa_chain()

    print(chain("Do you provide internships?"))