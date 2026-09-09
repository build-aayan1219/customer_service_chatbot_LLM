import hashlib
import json
import logging
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from docx import Document as DocxDocument
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from src.langchain_helper import get_embeddings


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONVERSATIONS_DIR = BASE_DIR / "conversations"


# ==================================================
# CONFIGURATION
# ==================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".csv",
    ".xlsx",
}

MAX_FILE_SIZE_MB = 20
MAX_FILES_PER_CHAT = 10

MAX_CHUNK_SIZE = 1400
CHUNK_OVERLAP = 180


# ==================================================
# LOGGING
# ==================================================

logger = logging.getLogger(__name__)


# ==================================================
# DIRECTORY HELPERS
# ==================================================

def _safe_chat_id(chat_id):
    """
    Convert chat ID into a filesystem-safe value.
    """

    value = str(chat_id or "").strip()

    if not value:
        raise ValueError("Chat ID is required.")

    value = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        value,
    )

    return value


def get_chat_directory(chat_id):
    return (
        CONVERSATIONS_DIR
        / _safe_chat_id(chat_id)
    )


def get_chat_files_directory(chat_id):
    return (
        get_chat_directory(chat_id)
        / "files"
    )


def get_chat_index_directory(chat_id):
    return (
        get_chat_directory(chat_id)
        / "index"
    )


def get_chat_manifest_path(chat_id):
    return (
        get_chat_directory(chat_id)
        / "manifest.json"
    )


def ensure_chat_directories(chat_id):
    get_chat_files_directory(chat_id).mkdir(
        parents=True,
        exist_ok=True,
    )

    get_chat_index_directory(chat_id).mkdir(
        parents=True,
        exist_ok=True,
    )


# ==================================================
# MANIFEST
# ==================================================

def _load_manifest(chat_id):
    ensure_chat_directories(chat_id)

    path = get_chat_manifest_path(chat_id)

    if not path.exists():
        return {
            "chat_id": str(chat_id),
            "files": [],
        }

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid manifest format.")

        if "files" not in data:
            data["files"] = []

        return data

    except Exception as error:
        logger.warning(
            "Could not read conversation manifest: %s",
            error,
        )

        return {
            "chat_id": str(chat_id),
            "files": [],
        }


def _save_manifest(chat_id, manifest):
    ensure_chat_directories(chat_id)

    path = get_chat_manifest_path(chat_id)

    with open(
        path,
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
# FILE HELPERS
# ==================================================

def _get_extension(filename):
    return Path(filename).suffix.lower()


def _calculate_sha256(data):
    return hashlib.sha256(data).hexdigest()


def _safe_filename(filename):
    """
    Prevent path traversal and unsafe filenames.
    """

    name = Path(str(filename)).name

    name = re.sub(
        r"[^a-zA-Z0-9._ -]",
        "_",
        name,
    )

    name = name.strip()

    if not name:
        name = "uploaded_file"

    return name[:180]


def _format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"

    return f"{size_bytes / (1024 * 1024):.1f} MB"


# ==================================================
# TEXT CHUNKING
# ==================================================

def _split_long_text(
    text,
    max_size=MAX_CHUNK_SIZE,
    overlap=CHUNK_OVERLAP,
):
    """
    Split long text while preserving a small overlap.
    """

    text = str(text or "").strip()

    if not text:
        return []

    if len(text) <= max_size:
        return [text]

    chunks = []

    start = 0

    while start < len(text):
        end = min(
            start + max_size,
            len(text),
        )

        if end < len(text):
            boundary = text.rfind(
                "\n",
                start,
                end,
            )

            if boundary == -1:
                boundary = text.rfind(
                    ". ",
                    start,
                    end,
                )

            if boundary > start + int(max_size * 0.55):
                end = boundary + (
                    1 if text[boundary] == "\n"
                    else 2
                )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def _chunk_paragraphs(paragraphs):
    """
    Build semantic-ish chunks from paragraphs.
    """

    chunks = []

    current = []

    current_length = 0

    for paragraph in paragraphs:
        paragraph = str(paragraph or "").strip()

        if not paragraph:
            continue

        if (
            current
            and current_length + len(paragraph) + 2
            > MAX_CHUNK_SIZE
        ):
            chunks.append(
                "\n".join(current).strip()
            )

            overlap_text = (
                current[-1]
                if current
                else ""
            )

            current = (
                [overlap_text]
                if overlap_text
                else []
            )

            current_length = len(
                overlap_text
            )

        current.append(paragraph)

        current_length += (
            len(paragraph) + 2
        )

    if current:
        chunks.append(
            "\n".join(current).strip()
        )

    final_chunks = []

    for chunk in chunks:
        if len(chunk) <= MAX_CHUNK_SIZE:
            final_chunks.append(chunk)
        else:
            final_chunks.extend(
                _split_long_text(chunk)
            )

    return [
        chunk
        for chunk in final_chunks
        if chunk.strip()
    ]


# ==================================================
# PDF EXTRACTION
# ==================================================

def _extract_pdf(path):
    documents = []

    reader = PdfReader(str(path))

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        try:
            text = page.extract_text() or ""
        except Exception as error:
            logger.warning(
                "Could not extract PDF page %d: %s",
                page_number,
                error,
            )
            text = ""

        text = text.strip()

        if not text:
            continue

        chunks = _split_long_text(text)

        for chunk_number, chunk in enumerate(
            chunks,
            start=1,
        ):
            documents.append(
                {
                    "text": chunk,
                    "location": (
                        f"Page {page_number}"
                        + (
                            f", section {chunk_number}"
                            if len(chunks) > 1
                            else ""
                        )
                    ),
                    "title": (
                        Path(path).stem
                    ),
                }
            )

    return documents


# ==================================================
# DOCX EXTRACTION
# ==================================================

def _extract_docx(path):
    document = DocxDocument(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    chunks = _chunk_paragraphs(
        paragraphs
    )

    return [
        {
            "text": chunk,
            "location": f"Section {index}",
            "title": Path(path).stem,
        }
        for index, chunk in enumerate(
            chunks,
            start=1,
        )
    ]


# ==================================================
# TXT / MARKDOWN EXTRACTION
# ==================================================

def _extract_text_file(path):
    text = Path(path).read_text(
        encoding="utf-8",
        errors="ignore",
    )

    paragraphs = [
        part.strip()
        for part in re.split(
            r"\n\s*\n",
            text,
        )
        if part.strip()
    ]

    if not paragraphs:
        paragraphs = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

    chunks = _chunk_paragraphs(
        paragraphs
    )

    return [
        {
            "text": chunk,
            "location": f"Section {index}",
            "title": Path(path).stem,
        }
        for index, chunk in enumerate(
            chunks,
            start=1,
        )
    ]


# ==================================================
# CSV EXTRACTION
# ==================================================

def _extract_csv(path):
    dataframe = pd.read_csv(
        path
    )

    documents = []

    for row_number, row in dataframe.iterrows():
        values = []

        for column in dataframe.columns:
            value = row[column]

            if pd.isna(value):
                continue

            values.append(
                f"{column}: {value}"
            )

        text = "\n".join(values).strip()

        if not text:
            continue

        documents.append(
            {
                "text": text,
                "location": (
                    f"Row {row_number + 2}"
                ),
                "title": Path(path).stem,
            }
        )

    return documents


# ==================================================
# XLSX EXTRACTION
# ==================================================

def _extract_xlsx(path):
    dataframe = pd.read_excel(
        path
    )

    documents = []

    for row_number, row in dataframe.iterrows():
        values = []

        for column in dataframe.columns:
            value = row[column]

            if pd.isna(value):
                continue

            values.append(
                f"{column}: {value}"
            )

        text = "\n".join(values).strip()

        if not text:
            continue

        documents.append(
            {
                "text": text,
                "location": (
                    f"Row {row_number + 2}"
                ),
                "title": Path(path).stem,
            }
        )

    return documents


# ==================================================
# DOCUMENT EXTRACTION
# ==================================================

def _extract_file(path):
    extension = _get_extension(
        path.name
    )

    if extension == ".pdf":
        return _extract_pdf(path)

    if extension == ".docx":
        return _extract_docx(path)

    if extension in {
        ".txt",
        ".md",
    }:
        return _extract_text_file(path)

    if extension == ".csv":
        return _extract_csv(path)

    if extension == ".xlsx":
        return _extract_xlsx(path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# ==================================================
# LANGCHAIN DOCUMENT CREATION
# ==================================================

def _build_documents(
    path,
    chat_id,
    file_hash,
):
    extracted = _extract_file(
        path
    )

    documents = []

    for index, item in enumerate(
        extracted,
        start=1,
    ):
        text = str(
            item.get("text", "")
        ).strip()

        if not text:
            continue

        metadata = {
            "source_type": "conversation_file",
            "chat_id": str(chat_id),
            "source_file": path.name,
            "file_name": path.name,
            "filename": path.name,
            "file_hash": file_hash,
            "location": item.get(
                "location",
                f"Section {index}",
            ),
            "title": item.get(
                "title",
                path.stem,
            ),
            "chunk_id": index,
        }

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return documents


# ==================================================
# VECTOR DATABASE
# ==================================================

def _index_exists(chat_id):
    index_dir = get_chat_index_directory(
        chat_id
    )

    return (
        (index_dir / "index.faiss").exists()
        and
        (index_dir / "index.pkl").exists()
    )


def _load_chat_vector_db(chat_id):
    if not _index_exists(chat_id):
        return None

    try:
        return FAISS.load_local(
            str(
                get_chat_index_directory(
                    chat_id
                )
            ),
            get_embeddings(),
            allow_dangerous_deserialization=True,
        )

    except Exception as error:
        logger.warning(
            "Could not load conversation FAISS: %s",
            error,
        )

        return None


def _save_chat_vector_db(
    chat_id,
    vector_db,
):
    ensure_chat_directories(
        chat_id
    )

    vector_db.save_local(
        str(
            get_chat_index_directory(
                chat_id
            )
        )
    )


def _clear_chat_index(chat_id):
    index_dir = get_chat_index_directory(
        chat_id
    )

    if index_dir.exists():
        shutil.rmtree(
            index_dir,
            ignore_errors=True,
        )

    index_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


def _rebuild_chat_index(chat_id):
    manifest = _load_manifest(
        chat_id
    )

    all_documents = []

    for file_info in manifest.get(
        "files",
        [],
    ):
        filename = file_info.get(
            "filename"
        )

        file_hash = file_info.get(
            "sha256"
        )

        if not filename or not file_hash:
            continue

        path = (
            get_chat_files_directory(
                chat_id
            )
            / filename
        )

        if not path.exists():
            continue

        try:
            documents = _build_documents(
                path,
                chat_id,
                file_hash,
            )

            all_documents.extend(
                documents
            )

        except Exception as error:
            logger.exception(
                "Failed rebuilding %s: %s",
                filename,
                error,
            )

    _clear_chat_index(
        chat_id
    )

    if not all_documents:
        logger.info(
            "Conversation %s has no indexed documents.",
            chat_id,
        )
        return None

    vector_db = FAISS.from_documents(
        all_documents,
        get_embeddings(),
    )

    _save_chat_vector_db(
        chat_id,
        vector_db,
    )

    logger.info(
        "Conversation FAISS rebuilt: chat=%s vectors=%d",
        chat_id,
        vector_db.index.ntotal,
    )

    return vector_db


# ==================================================
# PUBLIC API
# ==================================================

def list_conversation_files(chat_id):
    manifest = _load_manifest(
        chat_id
    )

    return manifest.get(
        "files",
        [],
    )


def get_conversation_file_count(chat_id):
    return len(
        list_conversation_files(
            chat_id
        )
    )


def add_conversation_files(
    chat_id,
    uploaded_files,
):
    """
    Save, process, embed and index uploaded files.

    Returns:
        {
            "added": [...],
            "skipped": [...],
            "errors": [...]
        }
    """

    ensure_chat_directories(
        chat_id
    )

    manifest = _load_manifest(
        chat_id
    )

    existing_files = manifest.get(
        "files",
        [],
    )

    existing_hashes = {
        item.get("sha256")
        for item in existing_files
    }

    existing_names = {
        item.get("filename")
        for item in existing_files
    }

    added = []
    skipped = []
    errors = []

    files_to_rebuild = False

    for uploaded_file in uploaded_files or []:
        filename = _safe_filename(
            getattr(
                uploaded_file,
                "name",
                "uploaded_file",
            )
        )

        extension = _get_extension(
            filename
        )

        if extension not in ALLOWED_EXTENSIONS:
            errors.append(
                f"{filename}: unsupported file type."
            )
            continue

        try:
            data = uploaded_file.getvalue()
        except Exception as error:
            errors.append(
                f"{filename}: could not read file ({error})."
            )
            continue

        size_bytes = len(data)

        if size_bytes == 0:
            errors.append(
                f"{filename}: file is empty."
            )
            continue

        if (
            size_bytes
            > MAX_FILE_SIZE_MB * 1024 * 1024
        ):
            errors.append(
                f"{filename}: file exceeds "
                f"{MAX_FILE_SIZE_MB} MB."
            )
            continue

        file_hash = _calculate_sha256(
            data
        )

        if file_hash in existing_hashes:
            skipped.append(
                f"{filename} already attached."
            )
            continue

        # Same filename with changed contents.
        # Remove the old version first.
        old_entries = [
            item
            for item in existing_files
            if item.get("filename") == filename
        ]

        if old_entries:
            old_path = (
                get_chat_files_directory(
                    chat_id
                )
                / filename
            )

            if old_path.exists():
                old_path.unlink()

            existing_files = [
                item
                for item in existing_files
                if item.get("filename") != filename
            ]

            files_to_rebuild = True

        path = (
            get_chat_files_directory(
                chat_id
            )
            / filename
        )

        try:
            path.write_bytes(
                data
            )

            # Verify that the saved file is
            # actually readable before indexing.
            documents = _build_documents(
                path,
                chat_id,
                file_hash,
            )

            if not documents:
                path.unlink(
                    missing_ok=True
                )

                errors.append(
                    f"{filename}: no readable text/content found."
                )
                continue

            file_info = {
                "filename": filename,
                "sha256": file_hash,
                "size_bytes": size_bytes,
                "size": _format_size(
                    size_bytes
                ),
                "extension": extension,
                "uploaded_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "chunks": len(
                    documents
                ),
            }

            existing_files.append(
                file_info
            )

            existing_hashes.add(
                file_hash
            )

            existing_names.add(
                filename
            )

            added.append(
                file_info
            )

            # We can incrementally add new documents
            # to the existing index.
            existing_db = (
                _load_chat_vector_db(
                    chat_id
                )
            )

            if (
                existing_db is not None
                and not files_to_rebuild
            ):
                existing_db.add_documents(
                    documents
                )

                _save_chat_vector_db(
                    chat_id,
                    existing_db,
                )

            else:
                files_to_rebuild = True

        except Exception as error:
            logger.exception(
                "Failed processing uploaded file %s",
                filename,
            )

            path.unlink(
                missing_ok=True
            )

            errors.append(
                f"{filename}: {error}"
            )

    if files_to_rebuild:
        manifest["files"] = existing_files

        _save_manifest(
            chat_id,
            manifest,
        )

        _rebuild_chat_index(
            chat_id
        )

    else:
        manifest["files"] = existing_files

        _save_manifest(
            chat_id,
            manifest,
        )

    logger.info(
        "Conversation files processed: chat=%s added=%d skipped=%d errors=%d",
        chat_id,
        len(added),
        len(skipped),
        len(errors),
    )

    return {
        "added": added,
        "skipped": skipped,
        "errors": errors,
    }


def remove_conversation_file(
    chat_id,
    filename,
):
    filename = _safe_filename(
        filename
    )

    manifest = _load_manifest(
        chat_id
    )

    files = manifest.get(
        "files",
        [],
    )

    remaining = [
        item
        for item in files
        if item.get("filename") != filename
    ]

    if len(remaining) == len(files):
        return False

    path = (
        get_chat_files_directory(
            chat_id
        )
        / filename
    )

    if path.exists():
        path.unlink()

    manifest["files"] = remaining

    _save_manifest(
        chat_id,
        manifest,
    )

    _rebuild_chat_index(
        chat_id
    )

    logger.info(
        "Removed conversation file: chat=%s file=%s",
        chat_id,
        filename,
    )

    return True


def load_conversation_vector_db(
    chat_id
):
    return _load_chat_vector_db(
        chat_id
    )


def delete_chat_storage(chat_id):
    chat_directory = get_chat_directory(
        chat_id
    )

    if chat_directory.exists():
        shutil.rmtree(
            chat_directory,
            ignore_errors=True,
        )

        logger.info(
            "Deleted conversation storage: %s",
            chat_id,
        )


def delete_all_chat_storage(
    chat_ids
):
    for chat_id in chat_ids or []:
        delete_chat_storage(
            chat_id
        )


# ==================================================
# DEBUG
# ==================================================

if __name__ == "__main__":
    print(
        "Conversation file engine ready."
    )