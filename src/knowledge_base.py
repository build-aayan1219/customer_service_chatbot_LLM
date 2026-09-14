import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

import re

from src.langchain_helper import create_vector_db


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "dataset.csv"
)

KB_DIR = (
    BASE_DIR
    / "knowledge_base"
)

UPLOAD_DIR = (
    KB_DIR
    / "uploads"
)

BASE_DATASET_PATH = (
    KB_DIR
    / "base_dataset.csv"
)

MANIFEST_PATH = (
    KB_DIR
    / "manifest.json"
)

VECTORDB_PATH = (
    BASE_DIR
    / "faiss_index"
)


# ==================================================
# PRODUCTION PIPELINE PATHS
# ==================================================

PIPELINE_DIR = KB_DIR / "pipeline"
QUARANTINE_DIR = PIPELINE_DIR / "quarantine"
VERSIONS_DIR = PIPELINE_DIR / "versions"
STAGING_DIR = PIPELINE_DIR / "staging"
PIPELINE_STATE_PATH = PIPELINE_DIR / "state.json"



# ==================================================
# CONFIGURATION
# ==================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "csv",
    "txt",
    "docx",
}


# ==================================================
# DIRECTORY SETUP
# ==================================================

def ensure_directories():

    KB_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    PIPELINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    QUARANTINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    VERSIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    STAGING_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def ensure_base_dataset():

    ensure_directories()

    if (
        not BASE_DATASET_PATH.exists()
        and DATASET_PATH.exists()
    ):

        shutil.copy2(
            DATASET_PATH,
            BASE_DATASET_PATH,
        )


# ==================================================
# MANIFEST
# ==================================================

def load_manifest():

    ensure_directories()

    if not MANIFEST_PATH.exists():
        return {}

    try:

        with MANIFEST_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (
        json.JSONDecodeError,
        OSError,
    ):

        pass

    return {}


def save_manifest(manifest):

    ensure_directories()

    with MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ==================================================
# FILE HASH
# ==================================================

def calculate_file_hash(file_data):

    return hashlib.sha256(
        file_data
    ).hexdigest()


# ==================================================
# PDF EXTRACTION
# ==================================================

def extract_pdf(file_path):

    from pypdf import PdfReader

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):

        text = page.extract_text() or ""

        text = text.strip()

        if text:

            pages.append(
                (
                    page_number,
                    text,
                )
            )

    return pages


# ==================================================
# DOCX EXTRACTION
# ==================================================

def extract_docx(file_path):

    from docx import Document

    document = Document(
        str(file_path)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    if not paragraphs:
        return []

    return [
        (
            1,
            "\n".join(paragraphs),
        )
    ]


# ==================================================
# TXT EXTRACTION
# ==================================================

def extract_txt(file_path):

    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    text = text.strip()

    if not text:
        return []

    return [
        (
            1,
            text,
        )
    ]


# ==================================================
# CSV EXTRACTION
# ==================================================

def extract_csv(file_path):

    dataframe = pd.read_csv(
        file_path
    )

    rows = []

    for row_number, row in dataframe.fillna(
        ""
    ).iterrows():

        parts = []

        for column in dataframe.columns:

            value = str(
                row[column]
            ).strip()

            if value:

                parts.append(
                    f"{column}: {value}"
                )

        text = "\n".join(
            parts
        ).strip()

        if text:

            rows.append(
                (
                    row_number + 2,
                    text,
                )
            )

    return rows


# ==================================================
# FILE EXTRACTION
# ==================================================

def extract_file(file_path):

    extension = (
        file_path
        .suffix
        .lower()
        .lstrip(".")
    )

    if extension == "pdf":
        return extract_pdf(file_path)

    if extension == "docx":
        return extract_docx(file_path)

    if extension == "txt":
        return extract_txt(file_path)

    if extension == "csv":
        return extract_csv(file_path)

    raise ValueError(
        f"Unsupported file type: .{extension}"
    )


# ==================================================
# TEXT CHUNKING
# ==================================================

def split_text(
    text,
    chunk_size=1800,
    overlap=250,
):
    """
    Split document text into retrieval-friendly chunks.

    Strategy:
    1. Detect numbered/markdown-style sections such as:
       "1. Product Overview"
       "2. Filter Replacement"
       "## Warranty"
    2. Keep each section together when it fits within chunk_size.
    3. If a section is too large, split it into smaller overlapping
       chunks while preserving the section heading.
    4. If no recognizable headings exist, fall back to paragraph-aware
       fixed-size chunking.

    This produces much more focused RAG sources than treating an entire
    uploaded document as one chunk.
    """

    text = text.strip()

    if not text:
        return []

    # Normalize line endings and excessive whitespace.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    # --------------------------------------------------
    # HEADING-AWARE SPLITTING
    # --------------------------------------------------
    #
    # Supports common knowledge-base/document headings:
    #   1. Product Overview
    #   2. Filter Replacement
    #   5. Common Issue: Device Will Not Turn On
    #   ## Warranty
    #   Section 1: Introduction
    #
    heading_pattern = re.compile(
        r"(?im)^[ \t]*("
        r"(?:#{1,6}[ \t]+.+)"
        r"|(?:\d{1,3}[.)][ \t]+.+)"
        r"|(?:section[ \t]+\d{1,3}(?:[.:)][ \t]*|[ \t]+).+)"
        r")[ \t]*$"
    )

    matches = list(heading_pattern.finditer(text))

    sections = []

    if matches:
        # Text before the first heading.
        prefix = text[:matches[0].start()].strip()

        if prefix:
            sections.append(
                {
                    "heading": "",
                    "text": prefix,
                }
            )

        for index, match in enumerate(matches):
            heading = match.group(1).strip()

            section_start = match.end()
            section_end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(text)
            )

            body = text[section_start:section_end].strip()

            section_text = (
                f"{heading}\n{body}".strip()
                if body
                else heading
            )

            if section_text:
                sections.append(
                    {
                        "heading": heading,
                        "text": section_text,
                    }
                )

    # --------------------------------------------------
    # SPLIT A LARGE BLOCK WITH OVERLAP
    # --------------------------------------------------

    def split_large_block(block, heading=""):
        block = block.strip()

        if not block:
            return []

        heading_prefix = f"{heading}\n" if heading else ""

        # If the whole section already fits, keep it as one focused chunk.
        if len(block) <= chunk_size:
            return [block]

        # Prefer paragraph boundaries before falling back to characters.
        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", block)
            if paragraph.strip()
        ]

        if not paragraphs:
            paragraphs = [block]

        chunks = []
        current = ""

        for paragraph in paragraphs:
            candidate = (
                f"{current}\n\n{paragraph}".strip()
                if current
                else paragraph
            )

            # Leave room for the heading in every sub-chunk.
            available_size = max(
                chunk_size - len(heading_prefix),
                300,
            )

            if len(candidate) <= available_size:
                current = candidate
                continue

            if current:
                chunks.append(
                    f"{heading_prefix}{current}".strip()
                    if heading
                    else current
                )

            # Paragraph itself may be larger than the available size.
            if len(paragraph) > available_size:
                start = 0

                while start < len(paragraph):
                    end = min(
                        start + available_size,
                        len(paragraph),
                    )

                    piece = paragraph[start:end].strip()

                    if piece:
                        chunks.append(
                            f"{heading_prefix}{piece}".strip()
                            if heading
                            else piece
                        )

                    if end >= len(paragraph):
                        break

                    start = max(
                        end - overlap,
                        start + 1,
                    )

                current = ""
            else:
                current = paragraph

        if current:
            chunks.append(
                f"{heading_prefix}{current}".strip()
                if heading
                else current
            )

        return chunks

    # If headings were found, split each section independently.
    if sections:
        chunks = []

        for section in sections:
            chunks.extend(
                split_large_block(
                    section["text"],
                    section["heading"],
                )
            )

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]

    # --------------------------------------------------
    # FALLBACK: PARAGRAPH-AWARE CHUNKING
    # --------------------------------------------------

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    if not paragraphs:
        paragraphs = [text]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = (
            f"{current}\n\n{paragraph}".strip()
            if current
            else paragraph
        )

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)

        if len(paragraph) <= chunk_size:
            current = paragraph
            continue

        # Character-level fallback for a very large paragraph.
        start = 0

        while start < len(paragraph):
            end = min(
                start + chunk_size,
                len(paragraph),
            )

            chunk = paragraph[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(paragraph):
                break

            start = max(
                end - overlap,
                start + 1,
            )

        current = ""

    if current:
        chunks.append(current)

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]


# ==================================================
# BUILD DATASET
# ==================================================

def build_dataset_from_sources():

    ensure_base_dataset()

    manifest = load_manifest()

    rows = []


    # ----------------------------------------------
    # ORIGINAL DATASET
    # ----------------------------------------------

    if BASE_DATASET_PATH.exists():

        base_dataframe = pd.read_csv(
            BASE_DATASET_PATH
        ).fillna("")

        for _, row in base_dataframe.iterrows():

            rows.append(
                row.to_dict()
            )


    # ----------------------------------------------
    # UPLOADED DOCUMENTS
    # ----------------------------------------------

    for filename, metadata in manifest.items():

        if not metadata.get(
            "active",
            True,
        ):

            continue

        file_path = (
            UPLOAD_DIR
            / filename
        )

        if not file_path.exists():
            continue

        extracted = extract_file(
            file_path
        )

        for page_number, text in extracted:

            chunks = split_text(
                text
            )

            for chunk_number, chunk in enumerate(
                chunks,
                start=1,
            ):

                rows.append(
                    {
                        "prompt": chunk,
                        "response": "",
                        "source_file": filename,
                        "location": (
                            f"Page/row {page_number}, "
                            f"chunk {chunk_number}"
                        ),
                    }
                )


    # ----------------------------------------------
    # CREATE DATAFRAME
    # ----------------------------------------------

    dataframe = pd.DataFrame(
        rows
    )

    if dataframe.empty:

        dataframe = pd.DataFrame(
            columns=[
                "prompt",
                "response",
            ]
        )


    DATASET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    dataframe.to_csv(
        DATASET_PATH,
        index=False,
    )


    return len(dataframe)


# ==================================================
# GET DOCUMENTS
# ==================================================

def get_documents():

    ensure_directories()

    manifest = load_manifest()

    documents = []


    for file_path in sorted(
        UPLOAD_DIR.iterdir(),
        key=lambda path: path.name.lower(),
    ):

        if not file_path.is_file():
            continue

        extension = (
            file_path
            .suffix
            .lower()
            .lstrip(".")
        )

        if extension not in ALLOWED_EXTENSIONS:
            continue

        metadata = manifest.get(
            file_path.name,
            {},
        )

        stat = file_path.stat()

        documents.append(
            {
                "name": file_path.name,
                "type": extension.upper(),
                "size": stat.st_size,
                "uploaded_at": metadata.get(
                    "uploaded_at",
                    "Unknown",
                ),
                "hash": metadata.get(
                    "hash",
                    "",
                ),
            }
        )


    return documents


# ==================================================
# FORMAT FILE SIZE
# ==================================================

def format_size(size):

    if size < 1024:

        return f"{size} B"

    if size < 1024 * 1024:

        return (
            f"{size / 1024:.1f} KB"
        )

    return (
        f"{size / (1024 * 1024):.1f} MB"
    )


# ==================================================
# ADD UPLOADED FILES
# ==================================================

def _pipeline_now():
    return datetime.now()


def _load_pipeline_state():
    ensure_directories()
    if not PIPELINE_STATE_PATH.exists():
        return {
            "current_version": 0,
            "pending": False,
            "pending_since": None,
            "attempt": 0,
            "next_retry_at": None,
            "last_run": None,
            "last_result": "never_run",
            "last_error": None,
            "last_quality": None,
            "last_run_id": None,
        }
    try:
        return json.loads(PIPELINE_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "current_version": 0,
            "pending": False,
            "attempt": 0,
            "next_retry_at": None,
            "last_result": "state_reset",
        }


def _save_pipeline_state(state):
    ensure_directories()
    PIPELINE_STATE_PATH.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _parse_hhmm(value):
    return datetime.strptime(str(value), "%H:%M").time()


def is_maintenance_window(now=None):
    from src.config import KB_PIPELINE_CONFIG
    now = now or _pipeline_now()
    start = _parse_hhmm(KB_PIPELINE_CONFIG["maintenance_window_start"])
    end = _parse_hhmm(KB_PIPELINE_CONFIG["maintenance_window_end"])
    current = now.time()
    if start <= end:
        return start <= current <= end
    return current >= start or current <= end


def _file_signature(path):
    stat = path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def detect_modified_documents():
    """Detect files changed outside the upload UI and stage them automatically."""
    ensure_directories()
    manifest = load_manifest()
    detected = []
    for filename, metadata in list(manifest.items()):
        if metadata.get("status") == "quarantined":
            continue
        path = UPLOAD_DIR / filename
        if not path.exists():
            if metadata.get("status") == "active":
                metadata["status"] = "pending"
                metadata["active"] = False
                metadata["pending_reason"] = "active file is missing; revalidation required"
                detected.append(filename)
            continue
        current_signature = _file_signature(path)
        current_hash = calculate_file_hash(path.read_bytes())
        if current_hash == metadata.get("hash"):
            if metadata.get("signature") != current_signature:
                metadata["signature"] = current_signature
            continue
        if current_hash != metadata.get("hash"):
            valid, reason = _validate_uploaded_file(path)
            if not valid:
                _quarantine_file(path, reason)
                metadata["status"] = "quarantined"
                metadata["active"] = False
                metadata["reason"] = reason
                detected.append(filename)
                continue
            metadata["hash"] = current_hash
            metadata["signature"] = current_signature
            metadata["status"] = "pending"
            metadata["active"] = False
            metadata["modified_at"] = _pipeline_now().strftime("%Y-%m-%d %H:%M:%S")
            metadata["pending_reason"] = "modified document detected"
            detected.append(filename)
    if detected:
        save_manifest(manifest)
        _set_pending(manifest, "external modification detection")
    return detected


def list_knowledge_base_versions():
    ensure_directories()
    versions = []
    for directory in sorted(VERSIONS_DIR.glob("v*"), reverse=True):
        if not directory.is_dir():
            continue
        metadata = {}
        version_file = directory / "version.json"
        if version_file.exists():
            try:
                metadata = json.loads(version_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                metadata = {}
        versions.append({
            "name": directory.name,
            "version": metadata.get("version"),
            "created_at": metadata.get("created_at", "Unknown"),
            "label": metadata.get("label", "version"),
        })
    return versions


def _quarantine_file(path, reason):
    ensure_directories()
    stamp = _pipeline_now().strftime("%Y%m%d_%H%M%S_%f")
    target_dir = QUARANTINE_DIR / stamp
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / path.name
    shutil.move(str(path), str(target))
    (target_dir / "reason.txt").write_text(str(reason), encoding="utf-8")
    return target


def _validate_uploaded_file(file_path):
    extension = file_path.suffix.lower().lstrip(".")
    if extension not in ALLOWED_EXTENSIONS:
        return False, "unsupported file type"
    try:
        extracted = extract_file(file_path)
        if not extracted:
            return False, "no readable content extracted"
        text = "\n".join(str(item[1]).strip() for item in extracted)
        if len(re.sub(r"\s+", "", text)) < 20:
            return False, "file contains insufficient readable content"
        return True, "valid"
    except Exception as error:
        return False, f"extraction failed: {error}"


def _set_pending(manifest, reason):
    for metadata in manifest.values():
        if metadata.get("status") == "active":
            continue
        if metadata.get("status") == "pending":
            metadata["pending_reason"] = reason

    state = _load_pipeline_state()
    if not state.get("pending"):
        state["pending_since"] = _pipeline_now().isoformat(timespec="seconds")
        state["attempt"] = 0
        state["next_retry_at"] = None
    state["pending"] = True
    state["last_result"] = "pending"
    _save_pipeline_state(state)


def add_uploaded_files(uploaded_files):
    """Stage new/modified files for the production KB pipeline.

    Files are validated and duplicate-checked, but are not activated immediately.
    Activation happens only through the pipeline during the configured maintenance window.
    """
    ensure_directories()
    manifest = load_manifest()
    added = 0
    skipped = []

    for uploaded_file in uploaded_files:
        filename = Path(uploaded_file.name).name
        extension = Path(filename).suffix.lower().lstrip(".")
        if extension not in ALLOWED_EXTENSIONS:
            skipped.append(f"{filename}: unsupported file type")
            continue

        file_data = uploaded_file.getvalue()
        content_hash = calculate_file_hash(file_data)

        duplicate = any(
            item.get("hash") == content_hash and item.get("status", "active") != "quarantined"
            for item in manifest.values()
        )
        if duplicate:
            skipped.append(f"{filename}: duplicate file")
            continue

        destination = UPLOAD_DIR / filename
        if destination.exists():
            old_hash = manifest.get(filename, {}).get("hash")
            if old_hash == content_hash:
                skipped.append(f"{filename}: duplicate file")
                continue
            stem, suffix = destination.stem, destination.suffix
            counter = 2
            while destination.exists() and manifest.get(filename, {}).get("hash") != content_hash:
                # A modified document keeps its logical filename when possible.
                break
            if destination.exists() and old_hash is not None:
                backup_dir = STAGING_DIR / "modified_backups"
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup = backup_dir / f"{filename}.{old_hash[:12]}.bak"
                if not backup.exists():
                    shutil.copy2(destination, backup)
        destination.write_bytes(file_data)

        valid, reason = _validate_uploaded_file(destination)
        timestamp = _pipeline_now().strftime("%Y-%m-%d %H:%M:%S")
        if not valid:
            quarantined = _quarantine_file(destination, reason)
            manifest[filename] = {
                "hash": content_hash,
                "uploaded_at": timestamp,
                "status": "quarantined",
                "active": False,
                "reason": reason,
                "quarantined_path": str(quarantined.relative_to(KB_DIR)),
            }
            skipped.append(f"{filename}: quarantined ({reason})")
            continue

        previous = manifest.get(filename, {})
        manifest[filename] = {
            **previous,
            "hash": content_hash,
            "uploaded_at": previous.get("uploaded_at", timestamp),
            "modified_at": timestamp,
            "status": "pending",
            "active": False,
            "signature": _file_signature(destination),
            "pending_reason": "new document" if not previous else "modified document",
        }
        added += 1

    save_manifest(manifest)
    if added:
        _set_pending(manifest, "document ingestion")
    return added, skipped


# ==================================================
# DELETE DOCUMENT
# ==================================================

def delete_document(
    filename
):

    file_path = (
        UPLOAD_DIR
        / filename
    )


    if file_path.exists():

        file_path.unlink()


    manifest = load_manifest()

    manifest.pop(
        filename,
        None,
    )

    save_manifest(
        manifest
    )


# ==================================================
# REBUILD KNOWLEDGE BASE
# ==================================================

def _build_candidate_dataset():
    """Build a candidate dataset without touching the active dataset."""
    ensure_base_dataset()
    manifest = load_manifest()
    rows = []

    if BASE_DATASET_PATH.exists():
        base_dataframe = pd.read_csv(BASE_DATASET_PATH).fillna("")
        rows.extend(row.to_dict() for _, row in base_dataframe.iterrows())

    for filename, metadata in manifest.items():
        if metadata.get("status", "active") == "quarantined":
            continue
        if metadata.get("status", "active") not in {"active", "pending"}:
            continue
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            continue
        extracted = extract_file(file_path)
        for page_number, text in extracted:
            chunks = split_text(text)
            for chunk_number, chunk in enumerate(chunks, start=1):
                rows.append({
                    "prompt": chunk,
                    "response": "",
                    "source_file": filename,
                    "location": f"Page/row {page_number}, chunk {chunk_number}",
                })

    dataframe = pd.DataFrame(rows)
    if dataframe.empty:
        dataframe = pd.DataFrame(columns=["prompt", "response"])
    return dataframe


def _token_set(text):
    return set(re.findall(r"\b[a-z0-9]{2,}\b", str(text).lower()))


def _overlap(left, right):
    a, b = _token_set(left), _token_set(right)
    if not a:
        return 0.0
    return len(a & b) / len(a)


def _quality_metrics(candidate):
    """Run deterministic pre-activation accuracy/grounding gates.

    Accuracy = retrieval coverage of representative known questions.
    Grounding = overlap between expected answers and retrieved candidate context.
    """
    if not BASE_DATASET_PATH.exists() or candidate.empty:
        return {"accuracy": 1.0, "grounding": 1.0, "samples": 0}

    base = pd.read_csv(BASE_DATASET_PATH).fillna("")
    samples = base[base["prompt"].astype(str).str.strip() != ""].head(25)
    if samples.empty:
        return {"accuracy": 1.0, "grounding": 1.0, "samples": 0}

    candidate_texts = candidate["prompt"].astype(str).tolist()
    accuracy_scores = []
    grounding_scores = []
    for _, row in samples.iterrows():
        query = str(row.get("prompt", ""))
        answer = str(row.get("response", ""))
        ranked = sorted(((_overlap(query, text), text) for text in candidate_texts), reverse=True)[:3]
        best = ranked[0][0] if ranked else 0.0
        accuracy_scores.append(best)
        if answer.strip() and ranked:
            grounding_scores.append(max(_overlap(answer, text) for _, text in ranked))
        else:
            grounding_scores.append(best)

    return {
        "accuracy": round(sum(accuracy_scores) / len(accuracy_scores), 4),
        "grounding": round(sum(grounding_scores) / len(grounding_scores), 4),
        "samples": len(samples),
    }


def _active_quality_metrics():
    if not DATASET_PATH.exists():
        return {"accuracy": 0.0, "grounding": 0.0, "samples": 0}
    return _quality_metrics(pd.read_csv(DATASET_PATH).fillna(""))


def _create_version_snapshot(label, state=None):
    ensure_directories()
    state = state or _load_pipeline_state()
    version = int(state.get("current_version", 0)) + 1
    version_dir = VERSIONS_DIR / f"v{version:04d}_{label}"
    version_dir.mkdir(parents=True, exist_ok=True)

    if DATASET_PATH.exists():
        shutil.copy2(DATASET_PATH, version_dir / "dataset.csv")
    if MANIFEST_PATH.exists():
        shutil.copy2(MANIFEST_PATH, version_dir / "manifest.json")
    if VECTORDB_PATH.exists():
        shutil.copytree(VECTORDB_PATH, version_dir / "faiss_index", dirs_exist_ok=True)
    uploads_snapshot = version_dir / "uploads"
    if UPLOAD_DIR.exists():
        shutil.copytree(UPLOAD_DIR, uploads_snapshot, dirs_exist_ok=True)

    metadata = {
        "version": version,
        "created_at": _pipeline_now().isoformat(timespec="seconds"),
        "label": label,
    }
    (version_dir / "version.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    return version, version_dir


def rollback_knowledge_base(version=None):
    ensure_directories()
    versions = sorted(VERSIONS_DIR.glob("v*"), reverse=True)
    if version is not None:
        versions = [item for item in versions if item.name.startswith(f"v{int(version):04d}_")]
    if not versions:
        raise FileNotFoundError("No KB version is available for rollback.")
    source = versions[0]

    if (source / "dataset.csv").exists():
        DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "dataset.csv", DATASET_PATH)
    if (source / "manifest.json").exists():
        shutil.copy2(source / "manifest.json", MANIFEST_PATH)
    if (source / "uploads").exists():
        if UPLOAD_DIR.exists():
            shutil.rmtree(UPLOAD_DIR)
        shutil.copytree(source / "uploads", UPLOAD_DIR)
    if (source / "faiss_index").exists():
        if VECTORDB_PATH.exists():
            shutil.rmtree(VECTORDB_PATH)
        shutil.copytree(source / "faiss_index", VECTORDB_PATH)

    state = _load_pipeline_state()
    state["current_version"] = max(0, int(source.name.split("_")[0][1:]))
    state["pending"] = False
    state["attempt"] = 0
    state["next_retry_at"] = None
    state["last_result"] = "rolled_back"
    state["last_run"] = _pipeline_now().isoformat(timespec="seconds")
    _save_pipeline_state(state)
    try:
        from src.langchain_helper import load_vector_db
        load_vector_db.cache_clear()
    except Exception:
        pass
    return source.name


def _activate_candidate(candidate, quality, label):
    state = _load_pipeline_state()
    version, version_dir = _create_version_snapshot(label, state)
    temp_dataset = STAGING_DIR / f"candidate_{version}.csv"
    candidate.to_csv(temp_dataset, index=False)
    shutil.copy2(temp_dataset, DATASET_PATH)
    try:
        create_vector_db()
    except Exception:
        rollback_knowledge_base(version)
        raise

    manifest = load_manifest()
    for metadata in manifest.values():
        if metadata.get("status") == "pending":
            metadata["status"] = "active"
            metadata["active"] = True
            metadata["activated_at"] = _pipeline_now().isoformat(timespec="seconds")
    save_manifest(manifest)

    state["current_version"] = version
    state["pending"] = False
    state["attempt"] = 0
    state["next_retry_at"] = None
    state["last_result"] = "activated"
    state["last_run"] = _pipeline_now().isoformat(timespec="seconds")
    state["last_error"] = None
    state["last_quality"] = quality
    state["last_run_id"] = version_dir.name
    _save_pipeline_state(state)
    return version


def run_knowledge_base_pipeline(force=False):
    """Execute the complete staged KB update lifecycle."""
    from src.config import KB_PIPELINE_CONFIG
    ensure_base_dataset()
    ensure_directories()
    detect_modified_documents()
    state = _load_pipeline_state()
    if not state.get("pending"):
        return {"status": "nothing_to_do", "state": state}

    now = _pipeline_now()
    retry_at = state.get("next_retry_at")
    if retry_at:
        try:
            if now < datetime.fromisoformat(retry_at):
                return {"status": "waiting_for_retry", "state": state}
        except ValueError:
            pass

    if not is_maintenance_window(now):
        state["last_result"] = "waiting_for_maintenance_window"
        _save_pipeline_state(state)
        return {"status": "waiting_for_maintenance_window", "state": state}

    try:
        candidate = _build_candidate_dataset()
        quality = _quality_metrics(candidate)
        baseline = _active_quality_metrics()
        min_accuracy = float(KB_PIPELINE_CONFIG["minimum_accuracy"] )
        min_grounding = float(KB_PIPELINE_CONFIG["minimum_grounding"] )
        accuracy_ok = quality["accuracy"] >= max(min_accuracy, baseline["accuracy"] - float(KB_PIPELINE_CONFIG["max_accuracy_drop"]))
        grounding_ok = quality["grounding"] >= max(min_grounding, baseline["grounding"] - float(KB_PIPELINE_CONFIG["max_grounding_drop"]))

        if not accuracy_ok or not grounding_ok:
            state["pending"] = False
            state["last_result"] = "rejected_quality"
            state["last_quality"] = {"candidate": quality, "baseline": baseline, "accuracy_ok": accuracy_ok, "grounding_ok": grounding_ok}
            state["last_run"] = now.isoformat(timespec="seconds")
            state["last_error"] = "Quality gate rejected candidate update."
            _save_pipeline_state(state)
            return {"status": "rejected_quality", "quality": quality, "baseline": baseline, "state": state}

        version = _activate_candidate(candidate, quality, "activated")
        return {"status": "activated", "version": version, "quality": quality, "baseline": baseline}
    except Exception as error:
        attempt = int(state.get("attempt", 0)) + 1
        delays = [15, 30, 60]
        if attempt <= len(delays):
            state["attempt"] = attempt
            state["next_retry_at"] = (now + timedelta(minutes=delays[attempt - 1])).isoformat(timespec="seconds")
            state["last_result"] = f"retry_scheduled_{delays[attempt - 1]}m"
            state["last_error"] = str(error)
        else:
            state["pending"] = False
            state["next_retry_at"] = None
            state["last_result"] = "failed_after_retries"
            state["last_error"] = str(error)
        state["last_run"] = now.isoformat(timespec="seconds")
        _save_pipeline_state(state)
        return {"status": state["last_result"], "error": str(error), "state": state}


def is_scheduled_run_due(now=None):
    from src.config import KB_PIPELINE_CONFIG
    now = now or _pipeline_now()
    scheduled = _parse_hhmm(KB_PIPELINE_CONFIG["scheduled_run_time"])
    state = _load_pipeline_state()
    last_scheduled = state.get("last_scheduled_date")
    return now.time() >= scheduled and last_scheduled != now.date().isoformat()


def run_scheduled_knowledge_base_pipeline():
    now = _pipeline_now()
    state = _load_pipeline_state()
    result = run_knowledge_base_pipeline(force=False)
    from src.config import KB_PIPELINE_CONFIG
    if now.time() >= _parse_hhmm(KB_PIPELINE_CONFIG["scheduled_run_time"]):
        state = _load_pipeline_state()
        state["last_scheduled_date"] = now.date().isoformat()
        _save_pipeline_state(state)
    return result


def get_pipeline_status():
    state = _load_pipeline_state()
    manifest = load_manifest()
    pending = sum(1 for item in manifest.values() if item.get("status") == "pending")
    quarantined = sum(1 for item in manifest.values() if item.get("status") == "quarantined")
    active = sum(1 for item in manifest.values() if item.get("status", "active") == "active")
    return {
        **state,
        "pending_documents": pending,
        "active_documents": active,
        "quarantined_documents": quarantined,
        "maintenance_window": is_maintenance_window(),
    }


def rebuild_knowledge_base():
    """Compatibility wrapper: queue and execute only inside maintenance window."""
    state = _load_pipeline_state()
    if not state.get("pending"):
        manifest = load_manifest()
        for metadata in manifest.values():
            if metadata.get("status") == "active":
                continue
        state["pending"] = True
        state["pending_since"] = _pipeline_now().isoformat(timespec="seconds")
        _save_pipeline_state(state)
    result = run_knowledge_base_pipeline()
    if result.get("status") != "activated":
        raise RuntimeError(result.get("error") or result.get("status"))
    return len(pd.read_csv(DATASET_PATH))


# ==================================================
# RENDER KNOWLEDGE BASE
# ==================================================

def render_knowledge_base():

    ensure_base_dataset()

    ensure_directories()


    # ==================================================
    # HEADER
    # ==================================================

    st.markdown(
        """
        <div class="dashboard-title">
            📚 Knowledge Base Manager
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="dashboard-subtitle">
            Upload, manage and rebuild the documents
            used by the AI customer support RAG system.
        </div>
        """,
        unsafe_allow_html=True,
    )


    detect_modified_documents()
    documents = get_documents()
    pipeline_status = get_pipeline_status()

    st.info(
        f"Pipeline: **{pipeline_status.get('last_result', 'unknown')}** · "
        f"Pending: **{pipeline_status.get('pending_documents', 0)}** · "
        f"Quarantined: **{pipeline_status.get('quarantined_documents', 0)}** · "
        f"Maintenance window active: **{'Yes' if pipeline_status.get('maintenance_window') else 'No'}**"
    )


    # ==================================================
    # STATISTICS
    # ==================================================

    base_entries = 0

    if BASE_DATASET_PATH.exists():

        try:

            base_entries = len(
                pd.read_csv(
                    BASE_DATASET_PATH
                )
            )

        except Exception:

            base_entries = 0


    dataset_entries = 0

    if DATASET_PATH.exists():

        try:

            dataset_entries = len(
                pd.read_csv(
                    DATASET_PATH
                )
            )

        except Exception:

            dataset_entries = 0


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Uploaded Documents",
            len(documents),
        )


    with col2:

        st.metric(
            "Base Entries",
            base_entries,
        )


    with col3:

        st.metric(
            "Indexed Entries",
            dataset_entries,
        )


    with col4:

        st.metric(
            "Vector Database",
            (
                "Ready"
                if VECTORDB_PATH.exists()
                else "Not Ready"
            ),
        )


    # ==================================================
    # UPLOAD
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '📤 Upload Documents'
        '</div>',
        unsafe_allow_html=True,
    )


    uploaded_files = st.file_uploader(
        "Upload knowledge-base files",
        type=list(
            ALLOWED_EXTENSIONS
        ),
        accept_multiple_files=True,
        help=(
            "Supported formats: PDF, CSV, TXT and DOCX."
        ),
    )


    if st.button(
        "⬆️ Add Documents",
        use_container_width=True,
        disabled=not uploaded_files,
    ):

        try:

            added, skipped = (
                add_uploaded_files(
                    uploaded_files
                )
            )


            if added:

                st.success(
                    f"Added {added} document(s)."
                )


            for message in skipped:

                st.warning(
                    message
                )


            if added:

                st.info(
                    "Documents are staged for the production pipeline. "
                    "They will be validated, quality-tested and activated only during the configured maintenance window."
                )


                st.rerun()


        except Exception as error:

            st.error(
                "Could not upload documents: "
                f"{error}"
            )


    # ==================================================
    # REBUILD
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '🔄 Build Knowledge Base'
        '</div>',
        unsafe_allow_html=True,
    )


    st.caption(
        "The production pipeline validates staged documents, runs accuracy and grounding gates, "
        "creates a rollback version, and activates approved changes only during the maintenance window."
    )


    if st.button(
        "▶️ Run Production Update",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Running validation, quality gates, versioning and activation..."
            ):

                row_count = (
                    rebuild_knowledge_base()
                )


            st.success(
                "Production knowledge-base update completed "
                f"with {row_count} indexed entries."
            )


            st.rerun()


        except Exception as error:

            st.error(
                "Could not rebuild knowledge base: "
                f"{error}"
            )


    # ==================================================
    # DOCUMENT LIST
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Uploaded Documents'
        '</div>',
        unsafe_allow_html=True,
    )


    if not documents:

        st.info(
            "No additional documents have been uploaded yet."
        )


    else:

        for document in documents:

            col1, col2, col3, col4 = st.columns(
                [4, 1, 1.5, 1.2]
            )


            with col1:

                st.markdown(
                    f"**{document['name']}**"
                )


            with col2:

                st.caption(
                    document["type"]
                )


            with col3:

                st.caption(
                    format_size(
                        document["size"]
                    )
                )


            with col4:

                if st.button(
                    "🗑️",
                    key=(
                        "delete_kb_"
                        + document["name"]
                    ),
                    help=(
                        f"Delete {document['name']}"
                    ),
                ):

                    try:

                        delete_document(
                            document["name"]
                        )

                        build_dataset_from_sources()

                        st.success(
                            f"Deleted {document['name']}."
                        )

                        st.rerun()


                    except Exception as error:

                        st.error(
                            "Could not delete document: "
                            f"{error}"
                        )


    # ==================================================
    # HOW IT WORKS
    # ==================================================

    st.markdown(
        '<div class="section-title">'
        'ℹ️ How It Works'
        '</div>',
        unsafe_allow_html=True,
    )


    st.info(
        "1. Upload PDF, CSV, TXT or DOCX files.\n\n"
        "2. New or modified files are validated and staged.\n\n"
        "3. Duplicate and invalid files are rejected or quarantined.\n\n"
        "4. A candidate KB is built and tested for accuracy and grounding.\n\n"
        "5. Approved changes are versioned and activated only during the maintenance window.\n\n"
        "6. Failed updates retry after 15, 30 and 60 minutes; activated versions can be rolled back."
    )