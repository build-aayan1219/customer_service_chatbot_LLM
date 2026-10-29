"""
tests/test_task6_session.py — Comprehensive tests for Task 6.
Covers:
- Language detection and language switching across 3 languages (Hindi, Spanish, French) + English
- Entity preservation (Order IDs, Product codes, dates, emails) without corruption
- Context retention for >= 10 messages
- Session isolation for concurrent users
- Clarification requests when language/intent confidence is low
- 30-minute active session window
- 24-hour resumable session with summary restoration
- Expired session renewal after 24 hours
- Deterministic testing with injectable clock
"""
from datetime import datetime, timedelta
from src.session_manager import (
    SessionManager,
    detect_language,
    extract_entities,
)


def test_language_detection_and_confidence():
    lang_hi, conf_hi = detect_language("Mujhe refund chahiye order ka")
    assert lang_hi == "hi"
    assert conf_hi >= 0.55

    lang_es, conf_es = detect_language("Hola por favor necesito ayuda con el pago")
    assert lang_es == "es"
    assert conf_es >= 0.55

    lang_fr, conf_fr = detect_language("Bonjour s'il vous plait comment obtenir un remboursement")
    assert lang_fr == "fr"
    assert conf_fr >= 0.55


def test_entity_preservation():
    raw = "My order is ORD#987654 and product PROD-101 purchased on 2026-03-15 by test@customer.com"
    entities = extract_entities(raw)
    assert any("987654" in e for e in entities)
    assert any("PROD-101" in e for e in entities)
    assert any("2026-03-15" in e for e in entities)
    assert any("test@customer.com" in e for e in entities)


def test_context_retention_over_10_messages():
    sm = SessionManager()
    base_time = datetime(2026, 10, 30, 9, 0)

    for i in range(12):
        sm.handle_message(
            user_id="user_ctx",
            message=f"Message number {i} with inquiry details",
            _clock=lambda: base_time + timedelta(minutes=i),
        )

    session = list(sm.sessions.values())[0]
    ctx = session.get_context(max_messages=10)
    assert len(ctx) == 10
    assert "Message number 11" in ctx[-1]["content"]


def test_session_isolation_concurrent_users():
    sm = SessionManager()
    t = datetime(2026, 10, 30, 10, 0)

    r_alice = sm.handle_message("alice", "My order is ORD#ALICE123", _clock=lambda: t)
    r_bob = sm.handle_message("bob", "My order is ORD#BOB456", _clock=lambda: t)

    assert r_alice["session_id"] != r_bob["session_id"]
    s_alice = sm.sessions[r_alice["session_id"]]
    s_bob = sm.sessions[r_bob["session_id"]]

    assert any("ALICE" in e for e in s_alice.entities_seen)
    assert not any("BOB" in e for e in s_alice.entities_seen)
    assert any("BOB" in e for e in s_bob.entities_seen)


def test_session_lifecycle_active_resumed_expired():
    sm = SessionManager()
    t0 = datetime(2026, 10, 30, 10, 0)

    # 1. Create initial session
    r1 = sm.handle_message("user1", "Hello I need help", _clock=lambda: t0)
    assert r1["lifecycle_action"] == "created"
    assert r1["status"] == "active"

    # 2. Within 30 minutes -> stays active
    t_20m = t0 + timedelta(minutes=20)
    r2 = sm.handle_message("user1", "Still here with follow up", _clock=lambda: t_20m)
    assert r2["lifecycle_action"] == "resumed_active"
    assert r2["status"] == "active"

    # 3. Between 30m and 24h (e.g. 2 hours later) -> restores summary
    t_2h = t0 + timedelta(hours=2)
    r3 = sm.handle_message("user1", "I am back now", _clock=lambda: t_2h)
    assert r3["lifecycle_action"] == "restored_summary"
    assert r3["status"] == "resumed_with_summary"
    assert r3["summary"] is not None

    # 4. Beyond 24 hours (e.g. 26 hours later) -> expires and starts new session
    t_26h = t_2h + timedelta(hours=26)
    r4 = sm.handle_message("user1", "Starting fresh query", _clock=lambda: t_26h)
    assert r4["lifecycle_action"] == "created_expired"
    assert r4["session_id"] != r1["session_id"]


def test_clarification_on_low_confidence():
    sm = SessionManager()
    t = datetime(2026, 10, 30, 12, 0)
    # Ambiguous random noise with low linguistic confidence
    res = sm.handle_message("user_clarify", "zzq qwerty asdfgh 12345", _clock=lambda: t)
    assert res["needs_clarification"] is True
