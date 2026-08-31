import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader


# Load environment variables
load_dotenv()

# Google Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Location of FAISS database
vectordb_file_path = "faiss_index"


def create_vector_db():

    # Load FAQ dataset
    loader = CSVLoader(
        file_path="dataset/dataset.csv",
        source_column="prompt"
    )

    data = loader.load()

    # Create vector database
    vectordb = FAISS.from_documents(
        documents=data,
        embedding=embeddings
    )

    # Save vector database
    vectordb.save_local(vectordb_file_path)


def get_answer(question):

    # Load the FAISS database
    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Find more relevant FAQ entries
    docs = vectordb.similarity_search(
        question,
        k=5
    )

    # Prepare context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Prompt Gemini
    prompt = f"""
You are a customer service chatbot for an e-learning company.

Answer the user's question using ONLY the information
available in the context below.

IMPORTANT:
- Give a direct and helpful answer.
- Use the information from the context.
- Do not invent information.
- If the context does not contain the answer, say:
  "I don't know based on the available information."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    # Get response from Gemini
    response = llm.invoke(prompt)

    # Handle Gemini response
    if isinstance(response.content, list):

        answer = ""

        for item in response.content:
            if isinstance(item, dict):
                answer += item.get("text", "")

        return answer.strip()

    return str(response.content).strip()