import hashlib
import logging
import re
import zipfile
import io
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
    raw_name = str(filename or "")
    name = Path(raw_name).name
    ext = Path(name).suffix.lower().lstrip(".")
    if not raw_name or name in {".", ".."}:
        return False, "Invalid filename."
    if any(part in raw_name.lower().replace("/", "\\") for part in ("..\\", ":\\")) or "/" in raw_name or "\\" in raw_name:
        return False, "Unsafe filename/path detected."
    if ext in UNSAFE_EXTENSIONS:
        return False, f"Unsafe file type '.{ext}' is not allowed."
    if ext not in ALLOWED_EVIDENCE_EXTENSIONS:
        return False, f"Unsupported evidence file type '.{ext}'."
    return True, ""


def _signature_matches(extension: str, data: bytes) -> bool:
    if extension == "pdf":
        return data.startswith(b"%PDF-")
    if extension in {"jpg", "jpeg"}:
        return data.startswith(b"\xff\xd8\xff")
    if extension == "png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if extension == "webp":
        return data.startswith(b"RIFF") and data[8:12] == b"WEBP"
    if extension == "docx":
        if not data.startswith(b"PK"):
            return False
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                return "[Content_Types].xml" in archive.namelist() and "word/document.xml" in archive.namelist()
        except Exception:
            return False
    return True


def validate_file_bytes(filename: str, data: bytes, max_mb: int = 25) -> tuple[bool, str]:
    ok, reason = is_safe_filename(filename)
    if not ok:
        return False, reason
    if not data:
        return False, "The uploaded file is empty."
    if len(data) > max_mb * 1024 * 1024:
        return False, f"File exceeds the {max_mb} MB limit."
    extension = Path(filename).suffix.lower().lstrip(".")
    if not _signature_matches(extension, data):
        return False, f"File content does not match the '.{extension}' file type."
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
