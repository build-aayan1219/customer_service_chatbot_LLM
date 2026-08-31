import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ---------------- GEMINI ----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

# ---------------- EMBEDDINGS ----------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- VECTOR DATABASE ----------------

vectordb_file_path = "faiss_index"


def create_vector_db():

    loader = CSVLoader(
        file_path="dataset/dataset.csv",
        source_column="prompt"
    )

    data = loader.load()

    vectordb = FAISS.from_documents(
        data,
        embeddings
    )

    vectordb.save_local(vectordb_file_path)

    return vectordb


# ---------------- QA CHAIN ----------------

def get_qa_chain():

    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

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

        response = llm.invoke(messages)

        return {
            "result": response.content,
            "source_documents": documents
        }

    return ask_question