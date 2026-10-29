"""
Task 3 - Structured Support Tickets, Priorities, Routing, and SLAs.
All time-dependent functions accept an optional `_clock` callable.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from src.config import TICKET_CONFIG
from src.task2_security import mask_sensitive_data

BASE_DIR = Path(__file__).resolve().parent.parent
TICKETS_DIR = BASE_DIR / "knowledge_base" / "tickets"
TICKETS_DIR.mkdir(parents=True, exist_ok=True)


def _now(clock=None):
    return clock() if clock else datetime.utcnow()


def is_business_time(dt, config=TICKET_CONFIG):
    if dt.weekday() in config.get("weekend_days", [5, 6]):
        return False
    if dt.strftime("%Y-%m-%d") in config.get("holidays", []):
        return False
    start_h, start_m = map(int, config["business_hours_start"].split(":"))
    end_h, end_m = map(int, config["business_hours_end"].split(":"))
    minutes = dt.hour * 60 + dt.minute
    return (start_h * 60 + start_m) <= minutes < (end_h * 60 + end_m)


def business_minutes_elapsed(start, end, config=TICKET_CONFIG):
    if end <= start:
        return 0.0
    elapsed = 0.0
    cursor = start
    step = timedelta(minutes=1)
    while cursor < end:
        if is_business_time(cursor, config):
            elapsed += 1
        cursor += step
        if elapsed > 100_000:
            break
    return elapsed


SEVERITY_WORDS = {
    "critical": ["critical", "urgent", "emergency", "cannot access", "down", "broken", "blocked"],
    "high": ["failed", "error", "unable", "not working", "issue", "problem", "wrong", "incorrect"],
    "low": ["question", "query", "wondering", "curious", "would like to know"],
}

SENTIMENT_SCORE = {
    "frustrated": 1, "negative": 1, "urgent": 2,
    "neutral": 0, "positive": -1, "sarcastic": 1,
}


def calculate_priority(issue_text, sentiment="neutral", wait_minutes=0, high_risk=False, config=TICKET_CONFIG):
    if high_risk:
        return "critical"
    text_lower = issue_text.lower()
    severity_score = 0
    for level, keywords in SEVERITY_WORDS.items():
        for kw in keywords:
            if kw in text_lower:
                if level == "critical":
                    severity_score = 3
                elif level == "high":
                    severity_score = max(severity_score, 2)
                else:
                    severity_score = max(severity_score, 1)
    sentiment_score = SENTIMENT_SCORE.get(sentiment, 0)
    wait_score = 2 if wait_minutes >= 60 else (1 if wait_minutes >= 15 else 0)
    total = severity_score + sentiment_score + wait_score
    if total >= 5:
        return "critical"
    if total >= 3:
        return "high"
    if total >= 1:
        return "medium"
    return "low"


def is_high_risk(text, config=TICKET_CONFIG):
    text_lower = text.lower()
    return any(kw in text_lower for kw in config.get("high_risk_keywords", []))


def route_ticket(issue_text, teams_config=None, unavailable_teams=None):
    if teams_config is None:
        teams_config = TICKET_CONFIG["teams"]
    unavailable = set(unavailable_teams or [])
    text_lower = issue_text.lower()
    best_team = None
    best_score = -1
    for team_name, team_info in teams_config.items():
        if team_name in unavailable or team_name == "escalation":
            continue
        skills = team_info.get("skills", [])
        score = sum(1 for s in skills if s in text_lower)
        if score > best_score:
            best_score = score
            best_team = team_name
    if best_team is None or best_team in unavailable:
        return "escalation"
    return best_team


_ORDER_RE = re.compile(r"\b(?:order[#\s-]*|ORD[#\s-]*)([A-Z0-9]{4,16})\b", re.I)
_EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s\-().]{7,}\d)")
_AMOUNT_RE = re.compile(r"(?:[₹$]|Rs\.?|INR|USD)\s*[\d,]+(?:\.\d{1,2})?|\d+(?:\.\d{1,2})?\s*(?:rupees?|dollars?)", re.I)


def extract_ticket_fields(messages):
    full_text = " ".join(m.get("content", "") for m in messages if m.get("role") == "user")
    order_ids = list({m.group(0) for m in _ORDER_RE.finditer(full_text)})
    emails = list({m.group(0) for m in _EMAIL_RE.finditer(full_text)})
    phones = list({m.group(0) for m in _PHONE_RE.finditer(full_text)})
    amounts = list({m.group(0) for m in _AMOUNT_RE.finditer(full_text)})
    issue_summary = ""
    for m in messages:
        if m.get("role") == "user":
            content = m.get("content", "").strip()
            if content and len(content) > 5:
                issue_summary = content[:300]
                break
    customer_contact = emails[0] if emails else (phones[0] if phones else "")
    return {
        "order_ids": order_ids,
        "customer_contact": customer_contact,
        "amounts": amounts,
        "issue_summary": issue_summary,
        "full_text": full_text,
    }


def missing_mandatory_fields(fields, config=TICKET_CONFIG):
    return [f for f in config.get("mandatory_fields", []) if not fields.get(f)]


def _issue_fingerprint(customer_contact, issue_text):
    normalised = re.sub(r"\s+", " ", issue_text.lower().strip())[:200]
    raw = f"{customer_contact.lower()}|{normalised}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def find_duplicate_ticket(tickets, customer_contact, issue_text):
    fp = _issue_fingerprint(customer_contact, issue_text)
    for t in tickets:
        if t.get("fingerprint") == fp and t.get("status") not in ("resolved", "closed"):
            return t
    return None


def create_ticket(conversation_id, messages, sentiment="neutral", unavailable_teams=None,
                  existing_tickets=None, _clock=None, config=TICKET_CONFIG):
    now = _now(_clock)
    fields = extract_ticket_fields(messages)
    missing = missing_mandatory_fields(fields, config)
    high_risk = is_high_risk(fields["full_text"], config)
    priority = calculate_priority(
        fields["issue_summary"] or fields["full_text"],
        sentiment=sentiment, wait_minutes=0, high_risk=high_risk, config=config,
    )
    existing = existing_tickets or []
    duplicate = find_duplicate_ticket(existing, fields["customer_contact"], fields["issue_summary"])
    if duplicate:
        return {**duplicate, "is_duplicate": True}
    team = route_ticket(
        fields["issue_summary"] or fields["full_text"],
        config.get("teams"), unavailable_teams,
    )
    ticket_id = str(uuid.uuid4())[:8]
    fingerprint = _issue_fingerprint(fields["customer_contact"], fields["issue_summary"])
    ticket = {
        "id": ticket_id,
        "conversation_id": conversation_id,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "status": "open",
        "priority": priority,
        "team": team,
        "is_duplicate": False,
        "is_high_risk": high_risk,
        "missing_fields": missing,
        "fingerprint": fingerprint,
        "sla_deadline": (now + timedelta(minutes=config["sla_minutes"][priority])).isoformat(),
        "escalated": high_risk or team == "escalation",
        "escalation_reason": "high_risk" if high_risk else ("no_team_available" if team == "escalation" else None),
        **fields,
    }
    _persist_ticket(ticket)
    return ticket


def _persist_ticket(ticket):
    path = TICKETS_DIR / f"{ticket['id']}.json"
    path.write_text(json.dumps(ticket, indent=2), encoding="utf-8")


def load_tickets():
    tickets = []
    for f in sorted(TICKETS_DIR.glob("*.json")):
        try:
            tickets.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return tickets


def sla_status(ticket, config=TICKET_CONFIG, _clock=None):
    now = _now(_clock)
    created = datetime.fromisoformat(ticket["created_at"])
    deadline = datetime.fromisoformat(ticket["sla_deadline"])
    sla_total = config["sla_minutes"][ticket["priority"]]
    elapsed_biz = business_minutes_elapsed(created, now, config)
    remaining_biz = max(0.0, sla_total - elapsed_biz)
    fraction_used = elapsed_biz / max(sla_total, 1)
    return {
        "ticket_id": ticket["id"],
        "priority": ticket["priority"],
        "sla_total_minutes": sla_total,
        "elapsed_business_minutes": round(elapsed_biz, 1),
        "remaining_business_minutes": round(remaining_biz, 1),
        "fraction_used": round(fraction_used, 3),
        "sla_warning": fraction_used >= config.get("sla_warning_threshold", 0.75),
        "sla_breached": now > deadline,
        "deadline": ticket["sla_deadline"],
    }


def check_and_escalate(ticket, config=TICKET_CONFIG, _clock=None):
    status = sla_status(ticket, config, _clock)
    if status["sla_breached"] and not ticket.get("escalated"):
        ticket["escalated"] = True
        ticket["escalation_reason"] = "sla_breach"
        ticket["updated_at"] = _now(_clock).isoformat()
        ticket["status"] = "escalated"
        _persist_ticket(ticket)
    return ticket


def generate_handoff_summary(ticket):
    masked_contact = mask_sensitive_data(ticket.get("customer_contact", "") or "")
    masked_summary = mask_sensitive_data(ticket.get("issue_summary", "") or "")
    amounts = ", ".join(ticket.get("amounts", [])) or "-"
    orders = ", ".join(ticket.get("order_ids", [])) or "-"
    lines = [
        f"=== Handoff Summary - Ticket {ticket['id']} ===",
        f"Priority   : {ticket['priority'].upper()}",
        f"Team       : {ticket['team']}",
        f"Status     : {ticket['status']}",
        f"Created    : {ticket.get('created_at', '-')}",
        f"SLA DL     : {ticket.get('sla_deadline', '-')}",
        f"Escalated  : {ticket.get('escalated', False)}",
        f"High-risk  : {ticket.get('is_high_risk', False)}",
        f"Contact    : {masked_contact or '[not provided]'}",
        f"Order IDs  : {orders}",
        f"Amounts    : {amounts}",
        f"Issue      : {masked_summary}",
    ]
    if ticket.get("missing_fields"):
        lines.append(f"Missing    : {', '.join(ticket['missing_fields'])}")
    return "\n".join(lines)
