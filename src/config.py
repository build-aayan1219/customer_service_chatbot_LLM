"""
Configuration file for the Customer Service Chatbot
Central place to manage all settings
"""

# ============================================================================
# CHAT SETTINGS
# ============================================================================

SUGGESTED_QUESTIONS = [
    {
        "emoji": "🎓",
        "text": "Do you provide internships?",
        "col": 0
    },
    {
        "emoji": "💳",
        "text": "Do you offer EMI?",
        "col": 1
    },
    {
        "emoji": "💻",
        "text": "Can I use Power BI on Mac?",
        "col": 0
    },
    {
        "emoji": "📊",
        "text": "Tableau vs Power BI?",
        "col": 1
    },
]

# ============================================================================
# LLM SETTINGS
# ============================================================================

LLM_CONFIG = {
    "model": "gemini-3.6-flash",
    "temperature": 0.1,
    "max_tokens": 2048,
}

# ============================================================================
# EMBEDDINGS SETTINGS
# ============================================================================

EMBEDDINGS_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
}

# ============================================================================
# VECTOR DB SETTINGS
# ============================================================================

RETRIEVER_CONFIG = {
    "k": 3,  # Number of documents to retrieve
}

SIMILARITY_THRESHOLD = 0.7

# ============================================================================
# UI SETTINGS
# ============================================================================

PAGE_CONFIG = {
    "page_title": "AI Customer Service Assistant",
    "page_icon": "🤖",
    "layout": "centered",
}

WELCOME_MESSAGE = """
How can I help you?
"""

WELCOME_SUBTEXT = """
Ask me about courses, internships, services,
tools and other available information.
"""

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    "api_rate_limit": "⚠️ **AI service temporarily unavailable**\n\nThe Gemini API usage limit has been reached. Please try again later.",
    "generic_error": "❌ **Unable to process your question**\n\nPlease try again.",
    "kb_not_found": "❌ Knowledge base not found. Click 'Create Knowledge Base' first!",
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    "kb_created": "Knowledge base updated successfully!",
}

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": "chatbot.log",
}

# ============================================================================
# DATASET SETTINGS
# ============================================================================

DATASET_CONFIG = {
    "csv_column": "prompt",  # Which column to use as source
}

# ============================================================================
# SESSION SETTINGS
# ============================================================================

SESSION_STATE_KEYS = ["messages", "sources"]

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    "enable_logging": True,
    "enable_source_display": True,
    "enable_suggested_questions": True,
    "enable_chat_history": True,
}