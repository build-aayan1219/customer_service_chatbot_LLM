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
# KNOWLEDGE BASE PRODUCTION PIPELINE
# ============================================================================

TASK2_CONFIG = {
    "enable_evidence_analysis": True,
    "enable_gemini_vision": True,
    "vision_model": "gemini-3.6-flash",
    "minimum_image_quality": 0.55,
    "processing_timeout_seconds": 30,
    "retention_hours": 24,
    "max_evidence_file_size_mb": 25,
    "background_job_retention_hours": 24,
}

# ============================================================================
# KNOWLEDGE BASE PRODUCTION PIPELINE
# ============================================================================

KB_PIPELINE_CONFIG = {
    "maintenance_window_start": "02:00",
    "maintenance_window_end": "04:00",  
    "scheduled_run_time": "01:55",
    "minimum_accuracy": 0.30,
    "minimum_grounding": 0.30,
    "max_accuracy_drop": 0.05,
    "max_grounding_drop": 0.05,
    "retry_delays_minutes": [15, 30, 60],
    "max_retries": 3,
    "quality_sample_size": 25,
    "auto_run_on_app_start": True,
    "health_check_window_seconds": 300,
    "health_check_max_latency_seconds": 5.0,
    "authorized_roles": ["admin", "kb_manager"],
    "default_role": "admin",
    "enable_prompt_injection_quarantine": True,
    "enable_pii_masking": True,
    "canary_query": "What courses do you offer?",
}

# ============================================================================
# TASK 3 — STRUCTURED SUPPORT TICKETS, PRIORITIES, ROUTING, AND SLAS
# ============================================================================

TICKET_CONFIG = {
    # SLA times in minutes per priority
    "sla_minutes": {
        "critical": 60,
        "high": 240,
        "medium": 1440,   # 24h
        "low": 4320,      # 72h
    },
    # Warn when this fraction of SLA time consumed
    "sla_warning_threshold": 0.75,
    # Business hours (local clock, 24h format)
    "business_hours_start": "09:00",
    "business_hours_end": "18:00",
    # 0=Mon…6=Sun; weekends excluded from SLA
    "weekend_days": [5, 6],
    # ISO date strings "YYYY-MM-DD" excluded from SLA
    "holidays": [],
    # Negative-sentiment threshold (minutes) before auto-escalation
    "unresolved_negative_escalation_minutes": 15,
    # Routing: team → skills list
    "teams": {
        "billing": {"skills": ["billing", "payment", "refund", "emi", "invoice"], "max_load": 10},
        "technical": {"skills": ["technical", "software", "tool", "error", "power bi", "tableau"], "max_load": 10},
        "general": {"skills": [], "max_load": 20},  # catch-all
        "escalation": {"skills": [], "max_load": 5},
    },
    # High-risk keywords that force escalation regardless of sentiment
    "high_risk_keywords": [
        "account compromise", "fraud", "legal", "lawsuit", "police",
        "duplicate payment", "double charge", "data breach", "chargeback",
    ],
    # Mandatory ticket fields
    "mandatory_fields": ["issue_summary", "customer_contact"],
}

# ============================================================================
# TASK 4 — METADATA-AWARE, ACCESS-CONTROLLED RAG ASSISTANT
# ============================================================================

RAG_CONFIG = {
    # Supported roles in order of privilege hierarchy
    "roles": ["customer", "support_agent", "supervisor", "admin"],
    "default_role": "customer",
    "access_hierarchy": {
        "customer": 1,
        "support_agent": 2,
        "supervisor": 3,
        "admin": 4,
    },
    # Allowed regions (or '*' for global)
    "default_region": "GLOBAL",
    "supported_regions": ["GLOBAL", "US", "EU", "APAC", "IN"],
    # Citations required for factual answers
    "require_citation": True,
    # Minimum grounding similarity threshold
    "minimum_grounding_score": 0.45,
    # When no policy matches, clarification/refusal response
    "refusal_message": "I do not have access to verified documentation to answer this question. Please contact our support team.",
    "missing_evidence_message": "Could you provide additional details or specify the relevant product/date so I can look up the correct policy for you?",
}


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