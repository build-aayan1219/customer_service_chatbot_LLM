import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd
import streamlit as st

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

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length,
        )

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        if end >= text_length:
            break

        start = max(
            end - overlap,
            start + 1,
        )

    return chunks


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

def add_uploaded_files(
    uploaded_files
):

    ensure_directories()

    manifest = load_manifest()

    added = 0

    skipped = []


    for uploaded_file in uploaded_files:

        extension = (
            Path(uploaded_file.name)
            .suffix
            .lower()
            .lstrip(".")
        )


        if extension not in ALLOWED_EXTENSIONS:

            skipped.append(
                f"{uploaded_file.name}: "
                "unsupported file type"
            )

            continue


        file_data = (
            uploaded_file.getvalue()
        )


        content_hash = (
            calculate_file_hash(
                file_data
            )
        )


        duplicate = any(
            item.get("hash") == content_hash
            for item in manifest.values()
        )


        if duplicate:

            skipped.append(
                f"{uploaded_file.name}: "
                "duplicate file"
            )

            continue


        filename = Path(
            uploaded_file.name
        ).name


        destination = (
            UPLOAD_DIR
            / filename
        )


        if destination.exists():

            stem = destination.stem

            suffix = destination.suffix

            counter = 2


            while destination.exists():

                destination = (
                    UPLOAD_DIR
                    / f"{stem}_{counter}{suffix}"
                )

                counter += 1


            filename = destination.name


        destination.write_bytes(
            file_data
        )


        manifest[filename] = {

            "hash":
                content_hash,

            "uploaded_at":
                pd.Timestamp.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "active":
                True,
        }


        added += 1


    save_manifest(
        manifest
    )


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

def rebuild_knowledge_base():

    row_count = (
        build_dataset_from_sources()
    )

    create_vector_db()

    return row_count


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


    documents = get_documents()


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
                    "Documents uploaded successfully. "
                    "Click 'Rebuild Knowledge Base' "
                    "to make them searchable."
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
        "Rebuilding combines your original dataset "
        "with uploaded documents and refreshes FAISS."
    )


    if st.button(
        "🔄 Rebuild Knowledge Base",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Extracting documents and rebuilding FAISS..."
            ):

                row_count = (
                    rebuild_knowledge_base()
                )


            st.success(
                "Knowledge base rebuilt successfully "
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
        "2. Click Add Documents.\n\n"
        "3. Click Rebuild Knowledge Base.\n\n"
        "4. Documents are extracted and split into searchable chunks.\n\n"
        "5. FAISS is rebuilt with the original dataset and uploaded documents.\n\n"
        "6. The chatbot can retrieve information from the updated knowledge base."
    )