import os
import logging
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate


# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENVIRONMENT & PATHS
# ============================================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "dataset.csv"
VECTORDB_PATH = BASE_DIR / "faiss_index"

logger.info(f"Dataset path: {DATASET_PATH}")
logger.info(f"Vector DB path: {VECTORDB_PATH}")


# ============================================================================
# GEMINI LLM
# ============================================================================

@lru_cache(maxsize=1)
def get_llm():
    """Get or create the Gemini LLM instance"""
    logger.info("Initializing Google Gemini LLM...")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )
    
    logger.info("✓ Gemini LLM initialized")
    return llm


# ============================================================================
# EMBEDDINGS
# ============================================================================

@lru_cache(maxsize=1)
def get_embeddings():
    """Get or create embeddings model"""
    logger.info("Loading HuggingFace embeddings model...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    logger.info("✓ Embeddings model loaded")
    return embeddings


# ============================================================================
# CREATE KNOWLEDGE BASE
# ============================================================================

def create_vector_db():
    """Create FAISS vector database from CSV dataset"""
    
    try:
        logger.info("=" * 60)
        logger.info("🚀 Starting vector database creation...")
        logger.info("=" * 60)
        
        # Load dataset
        logger.info(f"Loading dataset from: {DATASET_PATH}")
        
        if not DATASET_PATH.exists():
            logger.error(f"Dataset file not found: {DATASET_PATH}")
            raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
        
        loader = CSVLoader(
            file_path=str(DATASET_PATH),
            source_column="prompt"
        )
        
        data = loader.load()
        logger.info(f"✓ Loaded {len(data)} documents from CSV")
        
        # Create embeddings
        logger.info("Loading embeddings model...")
        embeddings = get_embeddings()
        
        # Create FAISS index
        logger.info("Creating FAISS vector database...")
        vectordb = FAISS.from_documents(
            data,
            embeddings
        )
        logger.info(f"✓ FAISS index created with {vectordb.index.ntotal} vectors")
        
        # Save locally
        logger.info(f"Saving FAISS index to: {VECTORDB_PATH}")
        vectordb.save_local(str(VECTORDB_PATH))
        logger.info("✓ FAISS index saved successfully")
        
        # Clear cached database
        load_vector_db.cache_clear()
        logger.info("✓ Cache cleared for next load")
        
        logger.info("=" * 60)
        logger.info("✓ Vector database creation COMPLETE")
        logger.info("=" * 60)
        
        return vectordb
    
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"❌ Error creating vector database: {e}")
        logger.error("=" * 60, exc_info=True)
        raise


# ============================================================================
# LOAD FAISS DATABASE
# ============================================================================

@lru_cache(maxsize=1)
def load_vector_db():
    """Load FAISS vector database from disk"""
    
    logger.info("Loading FAISS vector database...")
    
    if not VECTORDB_PATH.exists():
        logger.error(f"Vector DB not found at {VECTORDB_PATH}")
        logger.info("Please create it first by calling create_vector_db()")
        raise FileNotFoundError(
            f"Vector database not found at {VECTORDB_PATH}. "
            "Please create it first."
        )
    
    vectordb = FAISS.load_local(
        str(VECTORDB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True
    )
    
    logger.info(f"✓ Loaded FAISS index with {vectordb.index.ntotal} vectors")
    return vectordb


# ============================================================================
# QA CHAIN
# ============================================================================

def get_qa_chain():
    """Create QA chain for answering questions"""
    
    try:
        logger.info("Creating QA chain...")
        
        # Load vector database
        vectordb = load_vector_db()
        logger.info("✓ Vector database loaded")
        
        # Create retriever
        retriever = vectordb.as_retriever(
            search_kwargs={"k": 3}
        )
        logger.info("✓ Retriever created (k=3)")
        
        # Create prompt template
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
        
        logger.info("✓ Prompt template created")
        
        def ask_question(question):
            """Answer a single question"""
            
            logger.info(f"📝 Question: {question[:60]}...")
            
            # Retrieve documents
            documents = retriever.invoke(question)
            logger.info(f"📚 Retrieved {len(documents)} documents")
            
            # Create context
            context = "\n\n".join(
                document.page_content
                for document in documents
            )
            logger.info(f"📋 Context size: {len(context)} characters")
            
            # Get messages from prompt
            messages = prompt.invoke({
                "context": context,
                "question": question
            })
            
            # Generate response
            logger.info("🤖 Generating response with Gemini...")
            response = get_llm().invoke(messages)
            
            # Extract text
            answer = response.content
            
            if isinstance(answer, list):
                text_parts = []
                for item in answer:
                    if isinstance(item, dict) and "text" in item:
                        text_parts.append(item["text"])
                answer = "".join(text_parts)
            
            answer = str(answer).strip()
            
            logger.info(f"✓ Answer generated ({len(answer)} characters)")
            logger.info(f"💬 Answer: {answer[:60]}...")
            
            return {
                "result": answer,
                "source_documents": documents
            }
        
        logger.info("✓ QA chain created and ready")
        return ask_question
    
    except Exception as e:
        logger.error(f"❌ Error creating QA chain: {e}", exc_info=True)
        raise


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    
    logger.info("\n" + "=" * 60)
    logger.info("TESTING QA CHAIN")
    logger.info("=" * 60)
    
    try:
        logger.info("Step 1: Creating vector database...")
        create_vector_db()
        
        logger.info("\nStep 2: Creating QA chain...")
        chain = get_qa_chain()
        
        logger.info("\nStep 3: Testing with sample question...")
        test_question = "Do you provide internships?"
        result = chain(test_question)
        
        logger.info(f"\nQuestion: {test_question}")
        logger.info(f"Answer: {result['result']}")
        logger.info(f"Sources: {len(result['source_documents'])}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ TEST PASSED")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)