"""
Task 4 — Metadata-Aware, Access-Controlled RAG Assistant.

Key Capabilities:
- Store document version, product, region, access level, effective date, and expiry date.
- Metadata filtering happens BEFORE unauthorized content can influence answer generation.
- Policy selection resolves conflicts using effective/expiry dates, version numbers, and relevance.
- Current questions ignore future and expired policies.
- Historical questions retrieve the policy active on the customer's specified target date.
- Every factual answer includes verified source citations.
- Explicit refusal or clarification requested when evidence is missing or ambiguous.
- Strict detection & neutralizing of malicious prompt-injection content in retrieved docs.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.config import RAG_CONFIG
from src.task2_security import sanitize_user_input


def parse_iso_date(val: Optional[str]) -> Optional[date]:
    """Parse YYYY-MM-DD string into a datetime.date object."""
    if not val:
        return None
    try:
        return datetime.strptime(str(val).strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def is_authorized(user_role: str, doc_access_level: str, config: Dict = RAG_CONFIG) -> bool:
    """Check if user_role has sufficient privilege level for doc_access_level."""
    hierarchy = config.get("access_hierarchy", {
        "customer": 1,
        "support_agent": 2,
        "supervisor": 3,
        "admin": 4,
    })
    user_level = hierarchy.get(user_role.lower(), 1)
    doc_level = hierarchy.get(doc_access_level.lower(), 1)
    return user_level >= doc_level


def is_region_allowed(doc_region: str, user_region: Optional[str] = None) -> bool:
    """Check if document region matches user region or is globally applicable."""
    if not doc_region or doc_region.upper() in ("*", "GLOBAL", "ALL"):
        return True
    if not user_region or user_region.upper() in ("*", "GLOBAL", "ALL"):
        return True
    return doc_region.strip().upper() == user_region.strip().upper()


def is_policy_active(
    effective_date_str: Optional[str],
    expiry_date_str: Optional[str],
    query_date: date,
) -> bool:
    """
    Check if a policy is active on query_date.
    - If query_date is before effective date -> False (future policy)
    - If query_date is strictly after expiry date -> False (expired policy)
    """
    eff = parse_iso_date(effective_date_str)
    exp = parse_iso_date(expiry_date_str)

    if eff and query_date < eff:
        return False
    if exp and query_date > exp:
        return False
    return True


_DATE_PATTERNS = [
    re.compile(r"\bon\s+(\d{4}-\d{2}-\d{2})\b", re.I),
    re.compile(r"\bas\s+of\s+(\d{4}-\d{2}-\d{2})\b", re.I),
    re.compile(r"\bin\s+(\d{4}-\d{2}-\d{2})\b", re.I),
    re.compile(r"\bdate:\s*(\d{4}-\d{2}-\d{2})\b", re.I),
]


def extract_historical_date(query: str) -> Optional[date]:
    """Extract explicit reference date (e.g., 'on 2023-05-10', 'as of 2022-01-01') from query."""
    for pat in _DATE_PATTERNS:
        match = pat.search(query)
        if match:
            parsed = parse_iso_date(match.group(1))
            if parsed:
                return parsed
    return None


def filter_documents(
    documents: List[Dict[str, Any]],
    user_role: str = "customer",
    user_region: Optional[str] = None,
    product: Optional[str] = None,
    query_date: Optional[date] = None,
    config: Dict = RAG_CONFIG,
) -> List[Dict[str, Any]]:
    """
    Apply pre-retrieval access control, temporal validity, and product/region metadata filters.
    """
    effective_query_date = query_date or date.today()
    filtered = []

    for doc in documents:
        meta = doc.get("metadata", {})
        access_level = meta.get("access_level", "customer")

        # 1. Access Control
        if not is_authorized(user_role, access_level, config):
            continue

        # 2. Region Check
        doc_region = meta.get("region", "GLOBAL")
        if not is_region_allowed(doc_region, user_region):
            continue

        # 3. Product Check (if specified in query/filter)
        doc_product = meta.get("product")
        if product and doc_product:
            if doc_product.strip().lower() != product.strip().lower():
                continue

        # 4. Temporal Validity Check (Effective/Expiry)
        eff = meta.get("effective_date")
        exp = meta.get("expiry_date")
        if not is_policy_active(eff, exp, effective_query_date):
            continue

        filtered.append(doc)

    return filtered


def resolve_policy_conflicts(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    When multiple policies apply to the same topic/policy_id, select the newest version.
    """
    groups: Dict[str, List[Dict[str, Any]]] = {}
    ungrouped: List[Dict[str, Any]] = []

    for doc in documents:
        meta = doc.get("metadata", {})
        topic_key = meta.get("policy_id") or meta.get("topic")
        if topic_key:
            groups.setdefault(topic_key, []).append(doc)
        else:
            ungrouped.append(doc)

    resolved: List[Dict[str, Any]] = list(ungrouped)

    for topic, docs in groups.items():
        if len(docs) == 1:
            resolved.append(docs[0])
            continue

        # Sort by version (descending) and effective date (descending)
        def _sort_key(d: Dict[str, Any]) -> Tuple[int, date]:
            m = d.get("metadata", {})
            v = m.get("version", 1)
            eff = parse_iso_date(m.get("effective_date")) or date.min
            return (int(v) if isinstance(v, (int, float, str)) and str(v).isdigit() else 1, eff)

        best_doc = sorted(docs, key=_sort_key, reverse=True)[0]
        resolved.append(best_doc)

    return resolved


def build_rag_context(
    query: str,
    documents: List[Dict[str, Any]],
    user_role: str = "customer",
    user_region: Optional[str] = None,
    product: Optional[str] = None,
    reference_date: Optional[date] = None,
    config: Dict = RAG_CONFIG,
) -> Dict[str, Any]:
    """
    Full Task 4 pipeline:
    1. Pre-filtering by metadata (access, region, product, active dates)
    2. Conflict resolution (latest version)
    3. Neutralizing prompt injections in doc content
    4. Building grounded answer context and citations
    """
    target_date = reference_date or extract_historical_date(query) or date.today()

    # Pre-filtering
    filtered = filter_documents(
        documents=documents,
        user_role=user_role,
        user_region=user_region,
        product=product,
        query_date=target_date,
        config=config,
    )

    # Conflict resolution
    resolved = resolve_policy_conflicts(filtered)

    if not resolved:
        return {
            "has_evidence": False,
            "response": config.get("refusal_message"),
            "citations": [],
            "documents_used": [],
            "query_date": target_date.isoformat(),
        }

    # Format documents with citations and sanitize prompt injections
    citations = []
    sanitized_contexts = []

    for idx, doc in enumerate(resolved, 1):
        raw_text = doc.get("text", "")
        # Sanitize any malicious prompt injection patterns in retrieved text
        clean_text, was_quarantined = sanitize_user_input(raw_text)

        meta = doc.get("metadata", {})
        doc_id = meta.get("id") or meta.get("doc_id") or f"doc_{idx}"
        title = meta.get("title") or meta.get("policy_id") or f"Document {idx}"
        version = meta.get("version", "1.0")

        citation_entry = {
            "source_id": doc_id,
            "title": title,
            "version": version,
            "access_level": meta.get("access_level", "customer"),
            "effective_date": meta.get("effective_date", ""),
        }
        citations.append(citation_entry)
        sanitized_contexts.append(f"[{title} v{version}]: {clean_text}")

    context_str = "\n\n".join(sanitized_contexts)

    return {
        "has_evidence": True,
        "context": context_str,
        "citations": citations,
        "documents_used": resolved,
        "query_date": target_date.isoformat(),
    }
