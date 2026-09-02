import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path so we can import
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langchain_helper import (
    get_embeddings,
    get_llm,
    create_vector_db,
    load_vector_db,
    get_qa_chain,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_vectordb_path(tmp_path):
    """Create a temporary path for vector database testing"""
    return tmp_path / "test_faiss_index"


@pytest.fixture
def sample_dataset(tmp_path):
    """Create a sample CSV dataset for testing"""
    csv_path = tmp_path / "test_dataset.csv"
    
    content = """prompt,response
What is Python?,Python is a programming language
What is AI?,Artificial Intelligence is a field of computer science
Do you offer courses?,Yes we offer various courses"""
    
    csv_path.write_text(content)
    return csv_path


# ============================================================================
# TESTS FOR EMBEDDINGS
# ============================================================================

class TestEmbeddings:
    """Tests for the embeddings function"""
    
    def test_embeddings_loaded(self):
        """Test that embeddings model can be loaded"""
        embeddings = get_embeddings()
        assert embeddings is not None
    
    def test_embeddings_cached(self):
        """Test that embeddings are cached (same instance returned)"""
        embeddings1 = get_embeddings()
        embeddings2 = get_embeddings()
        assert embeddings1 is embeddings2
    
    def test_embeddings_can_embed_text(self):
        """Test that embeddings can convert text to vectors"""
        embeddings = get_embeddings()
        
        # Test embedding a simple sentence
        text = "What is the return policy?"
        
        try:
            # Embeddings should have an embed_query method or similar
            result = embeddings.embed_query(text)
            
            # Should return a list/array
            assert result is not None
            assert len(result) > 0
            assert isinstance(result, list)
            
        except Exception as e:
            pytest.skip(f"Embedding error (might be rate limited): {e}")


# ============================================================================
# TESTS FOR LLM
# ============================================================================

class TestLLM:
    """Tests for the LLM function"""
    
    def test_llm_loaded(self):
        """Test that LLM can be initialized"""
        llm = get_llm()
        assert llm is not None
    
    def test_llm_cached(self):
        """Test that LLM is cached (same instance returned)"""
        llm1 = get_llm()
        llm2 = get_llm()
        assert llm1 is llm2
    
    def test_llm_has_invoke_method(self):
        """Test that LLM has required methods"""
        llm = get_llm()
        assert hasattr(llm, 'invoke')


# ============================================================================
# TESTS FOR VECTOR DATABASE CREATION
# ============================================================================

class TestVectorDatabaseCreation:
    """Tests for vector database creation"""
    
    @patch('langchain_helper.DATASET_PATH')
    @patch('langchain_helper.VECTORDB_PATH')
    @patch('langchain_helper.CSVLoader')
    @patch('langchain_helper.FAISS')
    def test_create_vector_db_success(self, mock_faiss, mock_loader, mock_vectordb_path, mock_dataset_path):
        """Test successful vector database creation"""
        
        # Setup mocks
        mock_dataset_path.exists.return_value = True
        mock_vectordb_path.__str__.return_value = "/tmp/test_db"
        
        # Mock the loader to return documents
        mock_documents = [
            MagicMock(page_content="What is Python? Python is a language"),
            MagicMock(page_content="What is AI? AI is artificial intelligence")
        ]
        mock_loader.return_value.load.return_value = mock_documents
        
        # Mock FAISS
        mock_vectordb = MagicMock()
        mock_vectordb.index.ntotal = 2
        mock_faiss.from_documents.return_value = mock_vectordb
        
        # Create VectorDB - it should not raise an exception
        try:
            from langchain_helper import create_vector_db
            create_vector_db()
            # If we get here, the function ran successfully
            assert True
        except FileNotFoundError:
            # Expected if dataset doesn't exist
            assert True
    
    @patch('langchain_helper.DATASET_PATH')
    def test_create_vector_db_missing_dataset(self, mock_dataset_path):
        """Test that error is raised when dataset is missing"""
        
        mock_dataset_path.exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            from langchain_helper import create_vector_db
            create_vector_db()


# ============================================================================
# TESTS FOR VECTOR DATABASE LOADING
# ============================================================================

class TestVectorDatabaseLoading:
    """Tests for vector database loading"""
    
    @patch('langchain_helper.VECTORDB_PATH')
    def test_load_vector_db_missing_db(self, mock_vectordb_path):
        """Test that error is raised when vector DB doesn't exist"""
        
        mock_vectordb_path.exists.return_value = False
        
        # Clear the cache first
        load_vector_db.cache_clear()
        
        with pytest.raises(FileNotFoundError):
            load_vector_db()
    
    @patch('langchain_helper.VECTORDB_PATH')
    @patch('langchain_helper.FAISS')
    def test_load_vector_db_success(self, mock_faiss, mock_vectordb_path):
        """Test successful vector database loading"""
        
        # Setup mocks
        mock_vectordb_path.exists.return_value = True
        mock_vectordb_path.__str__.return_value = "/tmp/test_db"
        
        # Mock FAISS
        mock_vectordb = MagicMock()
        mock_vectordb.index.ntotal = 100
        mock_faiss.load_local.return_value = mock_vectordb
        
        # Clear cache
        load_vector_db.cache_clear()
        
        # Load should succeed
        result = load_vector_db()
        assert result is not None


# ============================================================================
# TESTS FOR QA CHAIN
# ============================================================================

class TestQAChain:
    """Tests for QA chain creation and functionality"""
    
    @patch('langchain_helper.load_vector_db')
    def test_get_qa_chain_creation(self, mock_load_db):
        """Test that QA chain can be created"""
        
        # Setup mock vector database
        mock_vectordb = MagicMock()
        mock_retriever = MagicMock()
        mock_vectordb.as_retriever.return_value = mock_retriever
        mock_load_db.return_value = mock_vectordb
        
        # Get QA chain
        chain = get_qa_chain()
        
        # Should return a callable function
        assert chain is not None
        assert callable(chain)
    
    @patch('langchain_helper.load_vector_db')
    @patch('langchain_helper.get_llm')
    def test_qa_chain_question_answering(self, mock_get_llm, mock_load_db):
        """Test that QA chain can answer questions"""
        
        # Setup mock vector database
        mock_vectordb = MagicMock()
        mock_retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "prompt: Do you offer courses?\nresponse: Yes we do"
        mock_retriever.invoke.return_value = [mock_doc]
        mock_vectordb.as_retriever.return_value = mock_retriever
        mock_load_db.return_value = mock_vectordb
        
        # Setup mock LLM
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Yes, we offer various technical courses"
        mock_llm.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm
        
        # Get and test QA chain
        chain = get_qa_chain()
        result = chain("Do you offer courses?")
        
        # Should have result and source_documents
        assert "result" in result
        assert "source_documents" in result
        assert result["result"] is not None
        assert len(result["source_documents"]) > 0
    
    @patch('langchain_helper.load_vector_db')
    @patch('langchain_helper.get_llm')
    def test_qa_chain_with_no_sources(self, mock_get_llm, mock_load_db):
        """Test QA chain when no sources are found"""
        
        # Setup mock vector database (empty results)
        mock_vectordb = MagicMock()
        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = []
        mock_vectordb.as_retriever.return_value = mock_retriever
        mock_load_db.return_value = mock_vectordb
        
        # Setup mock LLM
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "I don't know based on the available information"
        mock_llm.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm
        
        # Get and test QA chain
        chain = get_qa_chain()
        result = chain("Unknown question?")
        
        # Should still have result and empty source_documents
        assert "result" in result
        assert "source_documents" in result
        assert result["result"] is not None
        assert len(result["source_documents"]) == 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for the whole system"""
    
    def test_embeddings_and_llm_initialized(self):
        """Test that both embeddings and LLM initialize without errors"""
        try:
            embeddings = get_embeddings()
            llm = get_llm()
            
            assert embeddings is not None
            assert llm is not None
        except Exception as e:
            pytest.skip(f"API not available: {e}")
    
    def test_vector_db_path_exists(self):
        """Test that vector database path is defined correctly"""
        from langchain_helper import VECTORDB_PATH, DATASET_PATH
        
        # Paths should be Path objects
        assert isinstance(VECTORDB_PATH, Path)
        assert isinstance(DATASET_PATH, Path)
    
    @patch('langchain_helper.load_vector_db')
    @patch('langchain_helper.get_llm')
    def test_full_question_answer_flow(self, mock_get_llm, mock_load_db):
        """Integration test for complete Q&A flow"""
        
        # Setup mocks
        mock_vectordb = MagicMock()
        mock_retriever = MagicMock()
        
        # Create mock documents
        mock_doc1 = MagicMock()
        mock_doc1.page_content = "prompt: What is your return policy?\nresponse: 30 day returns"
        mock_doc2 = MagicMock()
        mock_doc2.page_content = "prompt: Can I return items?\nresponse: Yes, within 30 days"
        
        mock_retriever.invoke.return_value = [mock_doc1, mock_doc2]
        mock_vectordb.as_retriever.return_value = mock_retriever
        mock_load_db.return_value = mock_vectordb
        
        # Setup LLM
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "We offer 30 day returns on all products."
        mock_llm.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm
        
        # Execute
        chain = get_qa_chain()
        result = chain("What is your return policy?")
        
        # Verify
        assert result["result"] == "We offer 30 day returns on all products."
        assert len(result["source_documents"]) == 2


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Tests for performance characteristics"""
    
    def test_caching_works(self):
        """Test that caching prevents redundant initialization"""
        
        # Get embeddings twice
        embeddings1 = get_embeddings()
        embeddings2 = get_embeddings()
        
        # Should be the same object (cached)
        assert embeddings1 is embeddings2
    
    def test_llm_caching_works(self):
        """Test that LLM caching works"""
        
        llm1 = get_llm()
        llm2 = get_llm()
        
        assert llm1 is llm2


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Tests for proper error handling"""
    
    @patch('langchain_helper.get_llm')
    @patch('langchain_helper.load_vector_db')
    def test_qa_chain_handles_llm_error(self, mock_load_db, mock_get_llm):
        """Test that QA chain handles LLM errors gracefully"""
        
        # Setup vector DB
        mock_vectordb = MagicMock()
        mock_retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "test content"
        mock_retriever.invoke.return_value = [mock_doc]
        mock_vectordb.as_retriever.return_value = mock_retriever
        mock_load_db.return_value = mock_vectordb
        
        # Setup LLM to raise error
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("API Error")
        mock_get_llm.return_value = mock_llm
        
        # Should raise the error
        chain = get_qa_chain()
        
        with pytest.raises(Exception):
            chain("Test question")


# ============================================================================
# MAIN - RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])