import hashlib
import json
import logging
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from docx import Document as DocxDocument
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONVERSATIONS_DIR = (
    BASE_DIR
    / "knowledge_base"
    / "conversations"
)


# ==================================================
# CONFIGURATION
# ==================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt",
    "csv",
}

MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = (
    MAX_FILE_SIZE_MB * 1024 * 1024
)

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150


# ==================================================
# LOGGING
# ==================================================

logger = logging.getLogger(__name__)


# ==================================================
# DIRECTORY HELPERS
# ==================================================

def get_chat_directory(chat_id):
    """
    Return the storage directory for a conversation.
    """

    safe_chat_id = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        str(chat_id),
    )

    directory = (
        CONVERSATIONS_DIR
        / safe_chat_id
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def get_files_directory(chat_id):
    directory = (
        get_chat_directory(chat_id)
        / "files"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def get_index_directory(chat_id):
    directory = (
        get_chat_directory(chat_id)
        / "index"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def get_manifest_path(chat_id):
    return (
        get_chat_directory(chat_id)
        / "manifest.json"
    )


# ==================================================
# MANIFEST
# ==================================================

def _load_manifest(chat_id):
    path = get_manifest_path(chat_id)

    if not path.exists():
        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception as error:

        logger.warning(
            "Could not load conversation manifest: %s",
            error,
        )

        return []


def _save_manifest(
    chat_id,
    records,
):
    path = get_manifest_path(chat_id)

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ==================================================
# PUBLIC FILE LIST
# ==================================================

def list_conversation_files(chat_id):
    """
    Return all files attached to a conversation.
    """

    records = _load_manifest(chat_id)

    cleaned = []

    for record in records:

        if not isinstance(record, dict):
            continue

        file_path = Path(
            record.get(
                "path",
                "",
            )
        )

        if file_path.exists():

            cleaned.append(
                record
            )

    return cleaned


# ==================================================
# FILE HASH
# ==================================================

def _calculate_sha256(data):
    return hashlib.sha256(
        data
    ).hexdigest()


# ==================================================
# FILE SIZE
# ==================================================

def _format_file_size(size):
    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


# ==================================================
# SAFE FILE NAME
# ==================================================

def _safe_filename(filename):

    filename = Path(
        str(filename)
    ).name

    filename = re.sub(
        r"[^a-zA-Z0-9._ -]",
        "_",
        filename,
    )

    return filename[:180]


# ==================================================
# TEXT CLEANING
# ==================================================

def _clean_text(text):

    text = str(
        text or ""
    )

    text = text.replace(
        "\x00",
        " ",
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# ==================================================
# TEXT CHUNKING
# ==================================================

def _split_text(
    text,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
):
    """
    Split text into overlapping searchable chunks.

    Paragraph boundaries are preferred.
    """

    text = _clean_text(text)

    if not text:
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(
            r"\n\s*\n",
            text,
        )
        if paragraph.strip()
    ]

    if not paragraphs:
        paragraphs = [text]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        if len(
            current
        ) + len(paragraph) + 2 <= chunk_size:

            if current:

                current += (
                    "\n\n"
                    + paragraph
                )

            else:

                current = paragraph

            continue

        if current:

            chunks.append(
                current.strip()
            )

        overlap_text = (
            current[-chunk_overlap:]
            if current
            else ""
        )

        if overlap_text:

            current = (
                overlap_text
                + "\n\n"
                + paragraph
            )

        else:

            current = paragraph

        # Very large individual paragraph.
        while len(current) > chunk_size:

            chunks.append(
                current[:chunk_size].strip()
            )

            current = current[
                max(
                    0,
                    chunk_size - chunk_overlap,
                ):
            ]

    if current.strip():

        chunks.append(
            current.strip()
        )

    return chunks


# ==================================================
# PDF EXTRACTION
# ==================================================

def _extract_pdf(path):
    documents = []

    reader = PdfReader(
        str(path)
    )

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):

        text = _clean_text(
            page.extract_text()
            or ""
        )

        if not text:
            continue

        chunks = _split_text(
            text
        )

        for chunk_number, chunk in enumerate(
            chunks,
            start=1,
        ):

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "location": (
                            f"Page {page_number}, "
                            f"chunk {chunk_number}"
                        ),
                    },
                )
            )

    return documents


# ==================================================
# DOCX EXTRACTION
# ==================================================

def _extract_docx(path):

    doc = DocxDocument(
        str(path)
    )

    paragraphs = []

    for paragraph in doc.paragraphs:

        text = _clean_text(
            paragraph.text
        )

        if text:
            paragraphs.append(
                text
            )

    full_text = "\n\n".join(
        paragraphs
    )

    chunks = _split_text(
        full_text
    )

    documents = []

    for chunk_number, chunk in enumerate(
        chunks,
        start=1,
    ):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "location": (
                        f"Document chunk "
                        f"{chunk_number}"
                    ),
                },
            )
        )

    # Also process tables.
    for table_number, table in enumerate(
        doc.tables,
        start=1,
    ):

        rows = []

        for row in table.rows:

            cells = [
                _clean_text(
                    cell.text
                )
                for cell in row.cells
            ]

            rows.append(
                " | ".join(cells)
            )

        table_text = "\n".join(
            row
            for row in rows
            if row.strip()
        )

        if table_text:

            chunks = _split_text(
                table_text
            )

            for chunk_number, chunk in enumerate(
                chunks,
                start=1,
            ):

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "location": (
                                f"Table {table_number}, "
                                f"chunk {chunk_number}"
                            ),
                        },
                    )
                )

    return documents


# ==================================================
# TXT EXTRACTION
# ==================================================

def _extract_txt(path):

    text = ""

    for encoding in (
        "utf-8",
        "utf-8-sig",
        "latin-1",
    ):

        try:

            text = path.read_text(
                encoding=encoding
            )

            break

        except UnicodeDecodeError:

            continue

    text = _clean_text(
        text
    )

    chunks = _split_text(
        text
    )

    documents = []

    for chunk_number, chunk in enumerate(
        chunks,
        start=1,
    ):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "location": (
                        f"Document chunk "
                        f"{chunk_number}"
                    ),
                },
            )
        )

    return documents


# ==================================================
# CSV EXTRACTION
# ==================================================

def _extract_csv(path):

    dataframe = pd.read_csv(
        path
    )

    documents = []

    for row_number, row in dataframe.iterrows():

        parts = []

        for column in dataframe.columns:

            value = row[column]

            if pd.isna(value):
                continue

            parts.append(
                f"{column}: {value}"
            )

        row_text = "\n".join(
            parts
        ).strip()

        if not row_text:
            continue

        documents.append(
            Document(
                page_content=row_text,
                metadata={
                    "location": (
                        f"Row {row_number + 2}"
                    ),
                },
            )
        )

    return documents


# ==================================================
# DOCUMENT EXTRACTION
# ==================================================

def _extract_documents(
    path,
    chat_id,
    file_name,
):
    extension = (
        path.suffix
        .lower()
        .lstrip(".")
    )

    if extension == "pdf":

        documents = _extract_pdf(
            path
        )

    elif extension == "docx":

        documents = _extract_docx(
            path
        )

    elif extension == "txt":

        documents = _extract_txt(
            path
        )

    elif extension == "csv":

        documents = _extract_csv(
            path
        )

    else:

        raise ValueError(
            f"Unsupported file type: "
            f".{extension}"
        )

    for index, document in enumerate(
        documents,
        start=1,
    ):

        document.metadata.update(
            {
                "source_type": (
                    "conversation_file"
                ),
                "source_file": file_name,
                "file_name": file_name,
                "filename": file_name,
                "chat_id": str(chat_id),
                "chunk_index": index,
            }
        )

    return documents


# ==================================================
# EMBEDDING HELPER
# ==================================================

def _get_embeddings():
    """
    Import lazily to avoid circular imports.

    langchain_helper imports conversation_files
    during retrieval, so importing embeddings at
    module load time would create a circular import.
    """

    from src.langchain_helper import (
        get_embeddings
    )

    return get_embeddings()


# ==================================================
# LOAD CHAT VECTOR STORE
# ==================================================

def load_conversation_vector_db(
    chat_id
):
    """
    Load the FAISS index belonging to one chat.

    Returns None when the conversation has no
    indexed files.
    """

    index_directory = (
        get_index_directory(
            chat_id
        )
    )

    index_file = (
        index_directory
        / "index.faiss"
    )

    pickle_file = (
        index_directory
        / "index.pkl"
    )

    if not (
        index_file.exists()
        and pickle_file.exists()
    ):

        return None

    try:

        vectordb = FAISS.load_local(
            str(index_directory),
            _get_embeddings(),
            allow_dangerous_deserialization=True,
        )

        return vectordb

    except Exception as error:

        logger.exception(
            "Could not load conversation FAISS: %s",
            error,
        )

        return None


# ==================================================
# CACHE CLEARING
# ==================================================

def _clear_vector_cache():

    try:

        from src.langchain_helper import (
            load_vector_db
        )

        load_vector_db.cache_clear()

    except Exception:
        pass


# ==================================================
# ADD CONVERSATION FILES
# ==================================================

def add_conversation_files(
    chat_id,
    uploaded_files,
):
    """
    Automatically process uploaded files and add
    them to the current conversation's FAISS index.

    No global knowledge-base rebuild occurs.
    """

    if not uploaded_files:

        return {
            "added": [],
            "skipped": [],
            "errors": [],
        }

    files_directory = get_files_directory(
        chat_id
    )

    records = _load_manifest(
        chat_id
    )

    existing_hashes = {
        record.get("sha256")
        for record in records
        if isinstance(record, dict)
    }

    new_documents = []

    added_records = []
    skipped_files = []
    errors = []

    for uploaded_file in uploaded_files:

        try:

            original_name = _safe_filename(
                uploaded_file.name
            )

            extension = (
                Path(original_name)
                .suffix
                .lower()
                .lstrip(".")
            )

            if extension not in ALLOWED_EXTENSIONS:

                errors.append(
                    f"❌ {original_name}: "
                    f"Unsupported file type."
                )

                continue

            data = uploaded_file.getvalue()

            if len(data) > MAX_FILE_SIZE_BYTES:

                errors.append(
                    f"❌ {original_name}: "
                    f"File is larger than "
                    f"{MAX_FILE_SIZE_MB} MB."
                )

                continue

            file_hash = _calculate_sha256(
                data
            )

            if file_hash in existing_hashes:

                skipped_files.append(
                    {
                        "name": original_name,
                        "reason": "duplicate",
                    }
                )

                continue

            stored_name = (
                f"{file_hash[:12]}_"
                f"{original_name}"
            )

            stored_path = (
                files_directory
                / stored_name
            )

            stored_path.write_bytes(
                data
            )

            documents = _extract_documents(
                stored_path,
                chat_id,
                original_name,
            )

            if not documents:

                stored_path.unlink(
                    missing_ok=True
                )

                errors.append(
                    f"❌ {original_name}: "
                    f"No readable text was found."
                )

                continue

            record_id = (
                file_hash[:16]
            )

            record = {
                "id": record_id,
                "file_name": original_name,
                "stored_name": stored_name,
                "path": str(stored_path),
                "sha256": file_hash,
                "extension": extension,
                "size": len(data),
                "size_display": _format_file_size(
                    len(data)
                ),
                "chunk_count": len(
                    documents
                ),
                "uploaded_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            for document in documents:

                document.metadata[
                    "file_id"
                ] = record_id

            records.append(
                record
            )

            existing_hashes.add(
                file_hash
            )

            added_records.append(
                record
            )

            new_documents.extend(
                documents
            )

        except Exception as error:

            logger.exception(
                "Failed to process uploaded file"
            )

            errors.append(
                f"❌ {getattr(uploaded_file, 'name', 'file')}: "
                f"{error}"
            )

    # Save manifest before indexing so the file
    # remains visible even if indexing fails.
    _save_manifest(
        chat_id,
        records,
    )

    # ----------------------------------------------
    # UPDATE CHAT VECTOR STORE
    # ----------------------------------------------

    if new_documents:

        try:

            index_directory = (
                get_index_directory(
                    chat_id
                )
            )

            existing_vectordb = (
                load_conversation_vector_db(
                    chat_id
                )
            )

            embeddings = _get_embeddings()

            if existing_vectordb is None:

                vectordb = FAISS.from_documents(
                    new_documents,
                    embeddings,
                )

            else:

                existing_vectordb.add_documents(
                    new_documents
                )

                vectordb = existing_vectordb

            vectordb.save_local(
                str(index_directory)
            )

            logger.info(
                "Conversation FAISS updated | "
                "chat=%s | added_chunks=%d",
                chat_id,
                len(new_documents),
            )

        except Exception as error:

            logger.exception(
                "Conversation FAISS update failed: %s",
                error,
            )

            errors.append(
                "⚠️ Files were saved, but "
                "search indexing failed. "
                "Please try uploading the file again."
            )

    return {
        "added": added_records,
        "skipped": skipped_files,
        "errors": errors,
    }


# ==================================================
# REMOVE ONE FILE
# ==================================================

def remove_conversation_file(
    chat_id,
    file_id,
):
    """
    Remove one attached file and rebuild only the
    current conversation's vector index.
    """

    records = _load_manifest(
        chat_id
    )

    target = None
    remaining = []

    for record in records:

        if str(
            record.get("id")
        ) == str(file_id):

            target = record

        else:

            remaining.append(
                record
            )

    if target is None:
        return False

    # Delete physical file.
    try:

        path = Path(
            target.get(
                "path",
                "",
            )
        )

        if path.exists():
            path.unlink()

    except Exception as error:

        logger.warning(
            "Could not delete physical file: %s",
            error,
        )

    _save_manifest(
        chat_id,
        remaining,
    )

    _rebuild_conversation_index(
        chat_id,
        remaining,
    )

    return True


# ==================================================
# REBUILD ONE CHAT INDEX
# ==================================================

def _rebuild_conversation_index(
    chat_id,
    records,
):
    """
    Rebuild only the current chat's index.

    This is used internally after deleting a file.
    It is NOT a user-facing knowledge-base rebuild.
    """

    index_directory = (
        get_index_directory(
            chat_id
        )
    )

    if index_directory.exists():

        shutil.rmtree(
            index_directory
        )

    index_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_documents = []

    for record in records:

        path = Path(
            record.get(
                "path",
                "",
            )
        )

        if not path.exists():
            continue

        try:

            documents = _extract_documents(
                path,
                chat_id,
                record.get(
                    "file_name",
                    path.name,
                ),
            )

            for document in documents:

                document.metadata[
                    "file_id"
                ] = record.get(
                    "id"
                )

            all_documents.extend(
                documents
            )

        except Exception as error:

            logger.warning(
                "Could not re-index %s: %s",
                path.name,
                error,
            )

    if not all_documents:
        return

    try:

        vectordb = FAISS.from_documents(
            all_documents,
            _get_embeddings(),
        )

        vectordb.save_local(
            str(index_directory)
        )

        logger.info(
            "Conversation index rebuilt | "
            "chat=%s | chunks=%d",
            chat_id,
            len(all_documents),
        )

    except Exception as error:

        logger.exception(
            "Failed rebuilding conversation index: %s",
            error,
        )


# ==================================================
# DELETE ALL CHAT FILES
# ==================================================

def delete_conversation_files(
    chat_id
):
    """
    Delete all files and indexes belonging
    to one conversation.
    """

    chat_directory = (
        CONVERSATIONS_DIR
        / re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            str(chat_id),
        )
    )

    if chat_directory.exists():

        shutil.rmtree(
            chat_directory
        )

    return True


# ==================================================
# DELETE ALL CONVERSATION FILES
# ==================================================

def delete_all_conversation_files(
    chat_ids=None
):
    """
    Delete conversation-file storage.

    When chat_ids are provided, only those chats
    are deleted.
    """

    if chat_ids is None:

        if CONVERSATIONS_DIR.exists():

            shutil.rmtree(
                CONVERSATIONS_DIR
            )

        CONVERSATIONS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        return True

    for chat_id in chat_ids:

        delete_conversation_files(
            chat_id
        )

    return True


# ==================================================
# UPLOAD SIGNATURE
# ==================================================

def get_attachment_signature(
    uploaded_files
):
    """
    Generate a deterministic signature for the
    current Streamlit uploader state.

    Prevents the same uploaded file from being
    processed repeatedly on Streamlit reruns.
    """

    if not uploaded_files:
        return ""

    signatures = []

    for uploaded_file in uploaded_files:

        try:

            data = uploaded_file.getvalue()

            file_hash = _calculate_sha256(
                data
            )

            signatures.append(
                (
                    str(
                        uploaded_file.name
                    ),
                    len(data),
                    file_hash,
                )
            )

        except Exception:

            signatures.append(
                (
                    str(
                        uploaded_file.name
                    ),
                    0,
                    "",
                )
            )

    signatures.sort()

    raw_signature = json.dumps(
        signatures,
        sort_keys=True,
    )

    return hashlib.sha256(
        raw_signature.encode(
            "utf-8"
        )
    ).hexdigest()