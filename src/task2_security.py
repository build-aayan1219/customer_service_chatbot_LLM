import hashlib
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_EVIDENCE_EXTENSIONS = {
    "pdf", "png", "jpg", "jpeg", "webp", "docx", "txt", "csv"
}

UNSAFE_EXTENSIONS = {
    "exe", "bat", "cmd", "com", "scr", "msi", "dll", "ps1", "vbs",
    "js", "jar", "apk", "sh", "bin", "iso", "hta", "reg", "lnk"
}

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(the\s+)?instructions",
    r"system\s+message",
    r"developer\s+message",
    r"assistant\s+instructions",
    r"reveal\s+(your|the)\s+(prompt|instructions|system)",
    r"show\s+(your|the)\s+(prompt|instructions)",
    r"disregard\s+.*instructions",
    r"follow\s+these\s+instructions",
    r"execute\s+this\s+command",
    r"run\s+this\s+command",
    r"send\s+.*password",
    r"send\s+.*credit\s+card",
]

PAYMENT_PATTERNS = [
    (r"\b(?:\d[ -]*?){13,19}\b", "[MASKED_CARD]"),
    (r"\b\d{3,4}\b(?=\s*(?:cvv|cvc|security\s+code))", "[MASKED_CVV]"),
    (r"\b(?:upi|vpa)\s*[:=]?\s*[\w.\-]+@[\w]+\b", "[MASKED_UPI]"),
    (r"\b(?:account|a/c)\s*(?:number|no\.?)?\s*[:=]?\s*\d{8,18}\b", "[MASKED_ACCOUNT]"),
]

PERSONAL_PATTERNS = [
    (r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "[MASKED_EMAIL]"),
    (r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)", "[MASKED_PHONE]"),
    (r"\b(?:aadhaar|aadhar)\s*(?:number|no\.?)?\s*[:=]?\s*\d{4}\s*\d{4}\s*\d{4}\b", "[MASKED_AADHAAR]"),
]


def is_safe_filename(filename: str) -> tuple[bool, str]:
    name = Path(str(filename or "")).name
    ext = Path(name).suffix.lower().lstrip(".")
    if not name or name in {".", ".."}:
        return False, "Invalid filename."
    if ext in UNSAFE_EXTENSIONS:
        return False, f"Unsafe file type '.{ext}' is not allowed."
    if ext not in ALLOWED_EVIDENCE_EXTENSIONS:
        return False, f"Unsupported evidence file type '.{ext}'."
    if any(part in name.lower() for part in ("..", "\\", "/")):
        return False, "Unsafe filename/path detected."
    return True, ""


def validate_file_bytes(filename: str, data: bytes, max_mb: int = 25) -> tuple[bool, str]:
    ok, reason = is_safe_filename(filename)
    if not ok:
        return False, reason
    if not data:
        return False, "The uploaded file is empty."
    if len(data) > max_mb * 1024 * 1024:
        return False, f"File exceeds the {max_mb} MB limit."
    return True, ""


def detect_prompt_injection(text: str) -> list[str]:
    found = []
    value = str(text or "")
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE | re.DOTALL):
            found.append(pattern)
    return found


def mask_sensitive_data(text: str) -> str:
    value = str(text or "")
    for pattern, replacement in PAYMENT_PATTERNS + PERSONAL_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def safe_log(logger_obj, level: str, message: str, *args):
    safe_message = mask_sensitive_data(message)
    safe_args = tuple(mask_sensitive_data(str(arg)) for arg in args)
    getattr(logger_obj, level.lower(), logger_obj.info)(safe_message, *safe_args)


def file_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
