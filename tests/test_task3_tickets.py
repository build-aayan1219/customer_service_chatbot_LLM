"""
tests/test_task3_tickets.py — Task 3 automated tests.
Uses injectable clocks; no real sleeping.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from datetime import datetime, timedelta
from src.ticket_manager import (
    calculate_priority, is_high_risk, route_ticket,
    extract_ticket_fields, missing_mandatory_fields,
    find_duplicate_ticket, create_ticket, sla_status,
    check_and_escalate, generate_handoff_summary,
    is_business_time, business_minutes_elapsed,
)
from src.config import TICKET_CONFIG


# ── helpers ──────────────────────────────────────────────────────────────────

def _msgs(text, email="user@example.com"):
    return [
        {"role": "user", "content": f"My email is {email}. {text}"},
    ]

def _cfg(**overrides):
    return {**TICKET_CONFIG, **overrides}


# ── priority ──────────────────────────────────────────────────────────────────

def test_high_risk_forces_critical():
    p = calculate_priority("I cannot access my account", high_risk=True)
    assert p == "critical"


def test_frustrated_sentiment_raises_priority():
    p_neutral = calculate_priority("There is an issue", sentiment="neutral")
    p_frust = calculate_priority("There is an issue", sentiment="frustrated")
    # frustrated should be >= neutral priority
    order = ["low", "medium", "high", "critical"]
    assert order.index(p_frust) >= order.index(p_neutral)


def test_urgent_sentiment_yields_high_or_critical():
    p = calculate_priority("My payment failed", sentiment="urgent")
    assert p in ("high", "critical")


def test_wait_time_increases_priority():
    p_nowait = calculate_priority("My payment failed", wait_minutes=0)
    p_wait = calculate_priority("My payment failed", wait_minutes=90)
    order = ["low", "medium", "high", "critical"]
    assert order.index(p_wait) >= order.index(p_nowait)


def test_low_severity_neutral_is_low_or_medium():
    p = calculate_priority("I have a question about courses", sentiment="neutral")
    assert p in ("low", "medium")


# ── high-risk detection ───────────────────────────────────────────────────────

def test_fraud_keyword_is_high_risk():
    assert is_high_risk("I think there is fraud on my account")


def test_duplicate_payment_is_high_risk():
    assert is_high_risk("I was charged a duplicate payment")


def test_neutral_text_is_not_high_risk():
    assert not is_high_risk("I have a question about EMI options")


def test_calm_high_risk_overrides_sentiment():
    """A politely-worded message with 'fraud' must still be high-risk."""
    text = "Hello, I believe there may be fraud on my account. Could you help?"
    assert is_high_risk(text)


# ── routing ───────────────────────────────────────────────────────────────────

def test_billing_issue_routes_to_billing():
    team = route_ticket("I have a billing and payment problem")
    assert team == "billing"


def test_technical_issue_routes_to_technical():
    team = route_ticket("Power BI is not working on my machine, error occurred")
    assert team == "technical"


def test_unavailable_team_falls_back_to_escalation():
    team = route_ticket(
        "I have a billing problem",
        unavailable_teams=["billing", "general", "technical"],
    )
    assert team == "escalation"


def test_all_teams_unavailable_escalation():
    team = route_ticket("random query", unavailable_teams=["billing", "technical", "general"])
    assert team == "escalation"


# ── field extraction ─────────────────────────────────────────────────────────

def test_extracts_email():
    fields = extract_ticket_fields(_msgs("My order failed", "alice@example.com"))
    assert fields["customer_contact"] == "alice@example.com"


def test_extracts_order_id():
    msgs = [{"role": "user", "content": "Order#ABC12345 is missing"}]
    fields = extract_ticket_fields(msgs)
    assert any("ABC12345" in oid for oid in fields["order_ids"])


def test_missing_mandatory_fields_detected():
    fields = {"issue_summary": "some issue", "customer_contact": ""}
    missing = missing_mandatory_fields(fields)
    assert "customer_contact" in missing


def test_no_missing_fields_when_complete():
    fields = {"issue_summary": "Payment failed", "customer_contact": "user@x.com"}
    assert missing_mandatory_fields(fields) == []


# ── duplicate detection ───────────────────────────────────────────────────────

def test_duplicate_ticket_detected():
    msgs = _msgs("My refund is not processed")
    t1 = create_ticket("conv-1", msgs, _clock=lambda: datetime(2026, 10, 29, 10, 0))
    t2 = create_ticket("conv-2", msgs, existing_tickets=[t1],
                       _clock=lambda: datetime(2026, 10, 29, 10, 1))
    assert t2["is_duplicate"] is True
    assert t2["id"] == t1["id"]


def test_different_issues_not_merged():
    msgs1 = _msgs("My refund is not processed")
    msgs2 = _msgs("I cannot log in to my account")
    t1 = create_ticket("conv-1", msgs1, _clock=lambda: datetime(2026, 10, 29, 10, 0))
    t2 = create_ticket("conv-2", msgs2, existing_tickets=[t1],
                       _clock=lambda: datetime(2026, 10, 29, 10, 1))
    assert t2.get("is_duplicate") is False


# ── SLA ───────────────────────────────────────────────────────────────────────

def test_sla_warning_at_75_percent():
    # critical SLA = 60 min; business hours Mon 09:00; advance 46 min (>75%)
    base = datetime(2026, 10, 26, 9, 0)   # Monday 09:00 UTC
    msgs = _msgs("System is down critically")
    ticket = create_ticket("conv-sla-warn", msgs, sentiment="urgent",
                           _clock=lambda: base)
    # Simulate 46 minutes later (still within SLA but >75%)
    future = datetime(2026, 10, 26, 9, 46)
    status = sla_status(ticket, _clock=lambda: future)
    assert status["sla_warning"] is True
    assert status["sla_breached"] is False


def test_sla_breach_triggers_escalation():
    base = datetime(2026, 10, 26, 9, 0)
    msgs = _msgs("System is down critically")
    ticket = create_ticket("conv-sla-breach", msgs, sentiment="urgent",
                           _clock=lambda: base)
    # Advance past critical SLA deadline (61 min)
    future = datetime(2026, 10, 26, 10, 5)
    check_and_escalate(ticket, _clock=lambda: future)
    assert ticket["escalated"] is True
    assert ticket["escalation_reason"] == "sla_breach"


def test_weekend_excluded_from_sla():
    # Saturday 09:00 — should count 0 business minutes
    sat = datetime(2026, 10, 25, 9, 0)
    sun = datetime(2026, 10, 25, 17, 0)
    elapsed = business_minutes_elapsed(sat, sun)
    assert elapsed == 0.0


def test_holiday_excluded_from_sla():
    cfg = _cfg(holidays=["2026-10-26"])
    mon = datetime(2026, 10, 26, 9, 0)
    later = datetime(2026, 10, 26, 12, 0)
    elapsed = business_minutes_elapsed(mon, later, cfg)
    assert elapsed == 0.0


def test_runtime_sla_change():
    """SLA minutes can be changed at runtime via config dict."""
    custom_cfg = _cfg(sla_minutes={"critical": 120, "high": 480, "medium": 2880, "low": 8640})
    base = datetime(2026, 10, 26, 9, 0)
    msgs = _msgs("System is critically broken")
    ticket = create_ticket("conv-rt-sla", msgs, sentiment="urgent",
                           _clock=lambda: base, config=custom_cfg)
    # With 120-min critical SLA, 90 min should not be breached
    future = datetime(2026, 10, 26, 10, 30)
    status = sla_status(ticket, config=custom_cfg, _clock=lambda: future)
    assert status["sla_breached"] is False
    assert status["sla_total_minutes"] == 120


# ── handoff summary ───────────────────────────────────────────────────────────

def test_handoff_summary_masks_email():
    msgs = _msgs("Payment failed", "secret@bank.com")
    ticket = create_ticket("conv-hsum", msgs, _clock=lambda: datetime(2026, 10, 29, 10, 0))
    summary = generate_handoff_summary(ticket)
    assert "secret@bank.com" not in summary
    assert "Ticket" in summary


def test_handoff_summary_contains_required_fields():
    msgs = _msgs("My order ABC1234 was not delivered", "cust@test.com")
    ticket = create_ticket("conv-hreq", msgs, _clock=lambda: datetime(2026, 10, 29, 10, 0))
    summary = generate_handoff_summary(ticket)
    for field in ["Priority", "Team", "Status", "SLA DL"]:
        assert field in summary
