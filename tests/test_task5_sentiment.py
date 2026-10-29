"""
tests/test_task5_sentiment.py — Comprehensive tests for Task 5.
Covers:
- Sentiment classification (positive, neutral, negative, frustrated, urgent, sarcastic)
- Multilingual detection (English, Hindi/Hinglish, Spanish)
- Confidence scores
- High risk override of calm sentiment (fraud, account compromise, double charge, legal)
- Business hours handling: after-hours urgent -> on_call; normal -> next_business_day
- 15-minute unresolved negative conversation auto-escalation
- Repeated negative message detection
- Fully deterministic testing via injectable clocks
"""
from datetime import datetime, timedelta
from src.sentiment_escalation import (
    analyze_sentiment,
    detect_risk,
    evaluate_escalation,
)


def test_sentiment_classification_basic():
    s_pos = analyze_sentiment("Thank you so much, this is great!")
    assert s_pos["label"] == "positive"
    assert s_pos["confidence"] > 0.6

    s_neg = analyze_sentiment("This product is terrible and useless.")
    assert s_neg["label"] == "negative"

    s_urg = analyze_sentiment("Please help me immediately, it is critical!")
    assert s_urg["label"] == "urgent"


def test_sentiment_sarcasm_and_frustration():
    s_sarc = analyze_sentiment("Wow great service, waiting for 3 hours!")
    assert s_sarc["label"] in ("sarcastic", "frustrated")

    s_frust = analyze_sentiment("I am asking again and again, nobody helps here, fed up!")
    assert s_frust["label"] == "frustrated"


def test_multilingual_sentiment():
    # Hindi / Hinglish
    s_hi_pos = analyze_sentiment("Dhanyawad bahut acha response mila")
    assert s_hi_pos["label"] == "positive"

    s_hi_neg = analyze_sentiment("Bahut bekar aur kharab service hai")
    assert s_hi_neg["label"] == "negative"

    s_hi_urg = analyze_sentiment("Jaldi aur turant help chahiye")
    assert s_hi_urg["label"] == "urgent"

    # Spanish
    s_es_pos = analyze_sentiment("Muchas gracias excelente atencion")
    assert s_es_pos["label"] == "positive"


def test_high_risk_overrides_calm_sentiment():
    """Polite message discussing double payment or legal threat must trigger immediate escalation."""
    polite_double_charge = "Hello good morning, could you please check why I had a duplicate payment on my card?"
    res = evaluate_escalation("conv-risk-1", [{"role": "user", "content": polite_double_charge}])
    assert res["escalate"] is True
    assert "duplicate_payment" in res["reason"]
    assert res["condition"] == "high_risk_rule"

    polite_legal = "Thank you for your time, I am sending a legal notice via my lawyer today."
    res_legal = evaluate_escalation("conv-risk-2", [{"role": "user", "content": polite_legal}])
    assert res_legal["escalate"] is True
    assert "legal_threat" in res_legal["reason"]


def test_account_compromise_trigger():
    msg = "Someone logged in and my account is compromised!"
    res = evaluate_escalation("conv-hack", [{"role": "user", "content": msg}])
    assert res["escalate"] is True
    assert "account_compromise" in res["reason"]


def test_after_hours_routing():
    # Sunday midnight (outside business hours)
    sunday_night = datetime(2026, 10, 25, 23, 0)

    # 1. Urgent after hours -> routes to on-call
    res_urg = evaluate_escalation(
        "conv-ah-urg",
        [{"role": "user", "content": "Help me immediately, emergency issue"}],
        _clock=lambda: sunday_night,
    )
    assert res_urg["escalate"] is True
    assert res_urg["queue"] == "on_call"

    # 2. Normal inquiry after hours -> scheduled for next business day
    res_norm = evaluate_escalation(
        "conv-ah-norm",
        [{"role": "user", "content": "Hello, do you offer internships?"}],
        _clock=lambda: sunday_night,
    )
    assert res_norm["escalate"] is False
    assert res_norm["queue"] == "next_business_day"


def test_15_minute_unresolved_escalation():
    start = datetime(2026, 10, 26, 10, 0) # Monday 10:00 (Business hours)
    after_16_min = start + timedelta(minutes=16)

    msgs = [{"role": "user", "content": "Still not working, this is broken and terrible."}]
    res = evaluate_escalation(
        "conv-15m",
        msgs,
        conversation_start_time=start,
        _clock=lambda: after_16_min,
    )
    assert res["escalate"] is True
    assert res["condition"] == "15_min_unresolved_threshold"
    assert "senior_support" in res["queue"]


def test_repeated_negative_messages():
    msgs = [
        {"role": "user", "content": "This is terrible service."},
        {"role": "assistant", "content": "I apologize, what can I do?"},
        {"role": "user", "content": "Nobody helps, completely useless and fed up!"},
    ]
    now = datetime(2026, 10, 26, 11, 0)
    res = evaluate_escalation("conv-rep", msgs, conversation_start_time=now, _clock=lambda: now)
    assert res["escalate"] is True
    assert res["condition"] == "repeated_negative_sentiment"
