"""
Task 5 — Multilingual Sentiment, Risk Detection, and Escalation.

Requirements:
- Classify sentiment: positive, neutral, negative, frustrated, urgent, sarcastic.
- Generate calibrated confidence scores for predictions.
- Detect high-risk topics: account compromise, duplicate payment, legal threat, data breach.
- High-risk signals override misleadingly calm sentiment.
- Outside business hours: route urgent complaints to on-call queue; schedule normal complaints for next working day.
- Unresolved negative/frustrated conversations > 15 minutes automatically escalate.
- Record structured escalation audit log (reason, condition, summary).
- Fully deterministic testing with injectable clock.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.config import TICKET_CONFIG
from src.task2_security import mask_sensitive_data
from src.ticket_manager import is_business_time

# Lexicons with multilingual support (English, Hindi/Hinglish, Spanish)
SENTIMENT_LEXICON = {
    "positive": [
        "thank", "thanks", "great", "awesome", "excellent", "helpful", "good",
        "dhanyawad", "shukriya", "badhiya", "acha", "accha", "gracias", "excelente", "bueno"
    ],
    "negative": [
        "bad", "terrible", "horrible", "worst", "useless", "poor", "disappointed",
        "bekar", "kharab", "ghatiya", "malo", "pesimo", "decepcionado"
    ],
    "frustrated": [
        "again and again", "waste of time", "how many times", "still waiting", "nobody helps",
        "ridiculous", "fed up", "pareshan", "baar baar", "tang aa gaya", "harto", "frustrado"
    ],
    "urgent": [
        "urgent", "immediately", "asap", "right now", "emergency", "critical",
        "turant", "jaldi", "urgente", "ahora mismo"
    ],
    "sarcastic": [
        "wow great service", "oh brilliant", "super helpful not", "wonderful company",
        "kya baat hai", "bohot khoob", "vaya maravilla", "genial sarcasmo"
    ],
}

HIGH_RISK_TRIGGERS = {
    "account_compromise": [
        "hacked", "unauthorized access", "account compromised", "stolen password",
        "someone logged in", "account hack", "otp shared", "cuenta hackeada"
    ],
    "duplicate_payment": [
        "duplicate payment", "charged twice", "double deduction", "debited twice",
        "do baar cut gaye", "paisa do baar kata", "doble cobro", "pago duplicado"
    ],
    "legal_threat": [
        "lawyer", "lawsuit", "court", "consumer forum", "police", "legal notice",
        "police complaint", "fir", "vakil", "abogado", "demanda legal"
    ],
    "data_breach": [
        "data leak", "data breach", "privacy violation", "selling my data", "gdpr breach"
    ],
}


def _now(clock: Optional[Callable[[], datetime]] = None) -> datetime:
    return clock() if clock else datetime.utcnow()


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Classify text into positive, neutral, negative, frustrated, urgent, or sarcastic,
    returning label and confidence score.
    """
    cleaned = text.lower()
    counts = {label: 0 for label in SENTIMENT_LEXICON}

    for label, keywords in SENTIMENT_LEXICON.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned):
                counts[label] += 1
            elif kw in cleaned and len(kw.split()) > 1:
                counts[label] += 2

    top_label, top_count = max(counts.items(), key=lambda item: item[1])

    if top_count == 0:
        return {"label": "neutral", "confidence": 0.85, "scores": counts}

    # Sarcasm and Frustration take precedence over generic negative/positive
    if counts["sarcastic"] > 0:
        top_label = "sarcastic"
        top_count = counts["sarcastic"]
    elif counts["frustrated"] > 0:
        top_label = "frustrated"
        top_count = counts["frustrated"]

    total = sum(counts.values())
    confidence = min(0.98, max(0.60, round(top_count / max(total, 1), 2)))

    return {"label": top_label, "confidence": confidence, "scores": counts}


def detect_risk(text: str) -> Tuple[bool, Optional[str]]:
    """Detect if text contains severe high-risk issues overriding sentiment."""
    cleaned = text.lower()
    for risk_type, phrases in HIGH_RISK_TRIGGERS.items():
        for phrase in phrases:
            if phrase in cleaned:
                return True, risk_type
    return False, None


def evaluate_escalation(
    conversation_id: str,
    messages: List[Dict[str, Any]],
    conversation_start_time: Optional[datetime] = None,
    _clock: Optional[Callable[[], datetime]] = None,
    config: Dict = TICKET_CONFIG,
) -> Dict[str, Any]:
    """
    Evaluate conversation for escalation triggers:
    1. High-risk topic -> escalate immediately regardless of calm sentiment
    2. Repeated negative/frustrated sentiment (>1 consecutive)
    3. Unresolved negative conversation running > 15 minutes
    4. After-hours routing: urgent -> on-call; normal -> next business day
    """
    now = _now(_clock)
    last_user_message = ""
    user_messages = []

    for m in messages:
        if m.get("role") == "user":
            c = m.get("content", "").strip()
            if c:
                user_messages.append(c)
                last_user_message = c

    combined_text = " ".join(user_messages)
    sentiment_result = analyze_sentiment(last_user_message or combined_text)
    sentiment_label = sentiment_result["label"]

    # 1. High Risk Check (Overrides sentiment)
    is_risk, risk_category = detect_risk(combined_text)
    if is_risk:
        return {
            "escalate": True,
            "reason": f"High risk detected: {risk_category}",
            "condition": "high_risk_rule",
            "queue": "urgent_safety",
            "sentiment": sentiment_result,
            "audit_summary": f"Immediate escalation triggered by {risk_category}.",
            "timestamp": now.isoformat(),
        }

    # 2. Timing & Inactivity / Unresolved Duration Check
    start_time = conversation_start_time or now
    elapsed_minutes = (now - start_time).total_seconds() / 60.0
    threshold = config.get("unresolved_negative_escalation_minutes", 15)

    if elapsed_minutes >= threshold and sentiment_label in ("negative", "frustrated", "urgent"):
        return {
            "escalate": True,
            "reason": f"Negative/frustrated issue unresolved for {round(elapsed_minutes, 1)} minutes",
            "condition": "15_min_unresolved_threshold",
            "queue": "senior_support",
            "sentiment": sentiment_result,
            "audit_summary": f"Conversation exceeded {threshold}m SLA window without resolution.",
            "timestamp": now.isoformat(),
        }

    # 3. Repeated negative sentiment check (>= 2 negative/frustrated user messages)
    neg_count = sum(
        1 for msg in user_messages[-3:]
        if analyze_sentiment(msg)["label"] in ("negative", "frustrated", "urgent", "sarcastic")
    )
    if neg_count >= 2:
        return {
            "escalate": True,
            "reason": "Repeated negative or frustrated customer messages",
            "condition": "repeated_negative_sentiment",
            "queue": "escalation",
            "sentiment": sentiment_result,
            "audit_summary": "Customer expressed persistent negative sentiment across multiple messages.",
            "timestamp": now.isoformat(),
        }

    # 4. Business Hours Routing Check
    in_business = is_business_time(now, config)
    if not in_business:
        if sentiment_label == "urgent":
            return {
                "escalate": True,
                "reason": "After-hours urgent inquiry",
                "condition": "after_hours_urgent",
                "queue": "on_call",
                "sentiment": sentiment_result,
                "audit_summary": "Urgent request routed to 24/7 on-call queue outside business hours.",
                "timestamp": now.isoformat(),
            }
        else:
            return {
                "escalate": False,
                "reason": "After-hours non-urgent inquiry scheduled for next working day",
                "condition": "after_hours_normal",
                "queue": "next_business_day",
                "sentiment": sentiment_result,
                "audit_summary": "Normal request queued for next working day.",
                "timestamp": now.isoformat(),
            }

    return {
        "escalate": False,
        "reason": "Standard automated handling",
        "condition": "standard_flow",
        "queue": "standard",
        "sentiment": sentiment_result,
        "audit_summary": "Conversation within normal operational parameters.",
        "timestamp": now.isoformat(),
    }
