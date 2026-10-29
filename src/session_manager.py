"""
Task 6 — Multilingual Conversations and Session Management.

Key Requirements:
- Choose 3 additional languages: Hindi (hi), Spanish (es), French (fr) in addition to English (en).
- Support mixed-language messages and language switching within the same conversation.
- Preserve entity integrity (names, order IDs, dates, product codes) without corrupting them.
- Maintain conversation history for at least 10 messages across turns.
- Isolate simultaneous customer sessions with unique session tokens.
- Request clarification when confidence in language or user intent is low.
- Session lifecycle:
  * Active session: within 30 minutes of last activity.
  * Resumable session: between 30 minutes and 24 hours of inactivity (restores summary).
  * Expired session: beyond 24 hours (forces new session creation).
- Configurable timings, thresholds, and languages.
- Fully deterministic testing with injectable clock.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

SESSION_CONFIG = {
    "supported_languages": {
        "en": "English",
        "hi": "Hindi",
        "es": "Spanish",
        "fr": "French",
    },
    "default_language": "en",
    "inactivity_timeout_minutes": 30,
    "session_restoration_hours": 24,
    "min_context_messages": 10,
    "confidence_threshold": 0.55,
}

# Regex to preserve exact entity tokens
ENTITY_PATTERNS = [
    re.compile(r"\b(?:ORD[#\s-]*|ORDER[#\s-]*)[A-Z0-9]{4,16}\b", re.I),
    re.compile(r"\b[A-Z0-9]{2,4}-[A-Z0-9]{3,6}\b"),  # Product codes like PROD-990
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),             # Dates
    re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b"), # Emails
]

LANGUAGE_HINTS = {
    "hi": ["kya", "kaise", "hai", "mujhe", "chahiye", "paisa", "aapka", "dhanyawad", "namaste", "nahi", "karo"],
    "es": ["hola", "gracias", "por", "favor", "como", "esta", "quiero", "pago", "ayuda", "donde", "precio"],
    "fr": ["bonjour", "merci", "s'il", "vous", "plait", "comment", "je", "veux", "remboursement", "aide"],
    "en": ["hello", "help", "order", "product", "course", "refund", "internship", "payment", "please", "what"],
}


def _now(clock: Optional[Callable[[], datetime]] = None) -> datetime:
    return clock() if clock else datetime.utcnow()


def detect_language(text: str, config: Dict = SESSION_CONFIG) -> Tuple[str, float]:
    """Detect language of text with confidence score."""
    cleaned = text.lower()
    words = set(re.findall(r"\b\w+\b", cleaned))
    if not words:
        return config.get("default_language", "en"), 1.0

    scores = {lang: 0 for lang in config["supported_languages"]}

    for lang, hints in LANGUAGE_HINTS.items():
        for hint in hints:
            if hint in words:
                scores[lang] += 2
            elif hint in cleaned and len(hint.split()) > 1:
                scores[lang] += 3

    # If any specific non-default language has matched words, prioritize it if it matches more specific tokens
    top_lang, top_score = max(scores.items(), key=lambda x: (x[1], x[0] != "en"))
    if top_score == 0:
        return "unknown", 0.3

    confidence = min(0.99, max(0.60, round(top_score / max(len(words), 1), 2)))
    return top_lang, confidence



def extract_entities(text: str) -> List[str]:
    """Extract and protect critical identifiers from corruption."""
    entities = []
    for pat in ENTITY_PATTERNS:
        for m in pat.finditer(text):
            entities.append(m.group(0))
    return list(dict.fromkeys(entities))


class Session:
    def __init__(
        self,
        session_id: str,
        user_id: str,
        created_at: datetime,
        config: Dict = SESSION_CONFIG,
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = created_at
        self.last_active_at = created_at
        self.messages: List[Dict[str, Any]] = []
        self.preferred_language = config.get("default_language", "en")
        self.entities_seen: List[str] = []
        self.status = "active"  # active, resumable, expired

    def add_message(
        self,
        role: str,
        content: str,
        timestamp: datetime,
        config: Dict = SESSION_CONFIG,
    ) -> Dict[str, Any]:
        detected_lang, conf = detect_language(content, config)
        if conf >= config.get("confidence_threshold", 0.55) and detected_lang != "unknown":
            self.preferred_language = detected_lang

        extracted = extract_entities(content)
        for e in extracted:
            if e not in self.entities_seen:
                self.entities_seen.append(e)

        msg_obj = {
            "role": role,
            "content": content,
            "timestamp": timestamp.isoformat(),
            "language": detected_lang,
            "confidence": conf,
            "entities": extracted,
        }
        self.messages.append(msg_obj)
        self.last_active_at = timestamp
        return msg_obj

    def get_context(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent messages (retaining context for at least 10 messages)."""
        return self.messages[-max_messages:]

    def generate_summary(self) -> str:
        """Create a compact conversation summary when restoring a session."""
        topics = [m.get("content", "")[:40] for m in self.messages if m.get("role") == "user"]
        summary_topics = "; ".join(topics[-3:]) or "General Inquiry"
        entities_str = ", ".join(self.entities_seen) or "None"
        return f"Prior Context: {summary_topics} | Tracked Identifiers: {entities_str}"


class SessionManager:
    def __init__(self, config: Dict = SESSION_CONFIG):
        self.config = config
        self.sessions: Dict[str, Session] = {}

    def get_or_create_session(
        self,
        user_id: str,
        _clock: Optional[Callable[[], datetime]] = None,
    ) -> Tuple[Session, str]:
        """
        Retrieves active session, restores resumable session with summary,
        or creates a new session if expired.
        Returns (session, lifecycle_action).
        """
        now = _now(_clock)
        existing = [s for s in self.sessions.values() if s.user_id == user_id]

        if not existing:
            new_s = Session(str(uuid.uuid4())[:8], user_id, now, self.config)
            self.sessions[new_s.session_id] = new_s
            return new_s, "created"

        # Sort by most recent activity
        session = sorted(existing, key=lambda s: s.last_active_at, reverse=True)[0]
        inactive_minutes = (now - session.last_active_at).total_seconds() / 60.0
        restoration_hours = self.config.get("session_restoration_hours", 24)
        timeout_minutes = self.config.get("inactivity_timeout_minutes", 30)

        # 1. Active: within 30 minutes
        if inactive_minutes <= timeout_minutes:
            session.status = "active"
            return session, "resumed_active"

        # 2. Resumable: within 24 hours -> restore with summary
        if inactive_minutes <= restoration_hours * 60:
            session.status = "resumed_with_summary"
            return session, "restored_summary"

        # 3. Expired: beyond 24 hours -> brand new session
        session.status = "expired"
        new_session = Session(str(uuid.uuid4())[:8], user_id, now, self.config)
        self.sessions[new_session.session_id] = new_session
        return new_session, "created_expired"

    def handle_message(
        self,
        user_id: str,
        message: str,
        _clock: Optional[Callable[[], datetime]] = None,
    ) -> Dict[str, Any]:
        now = _now(_clock)
        session, action = self.get_or_create_session(user_id, _clock)
        msg_record = session.add_message("user", message, now, self.config)

        # Confidence check for low language/intent clarity
        needs_clarification = msg_record["confidence"] < self.config.get("confidence_threshold", 0.55)

        return {
            "session_id": session.session_id,
            "lifecycle_action": action,
            "status": session.status,
            "preferred_language": session.preferred_language,
            "needs_clarification": needs_clarification,
            "context_count": len(session.get_context()),
            "preserved_entities": session.entities_seen,
            "summary": session.generate_summary() if action == "restored_summary" else None,
        }
