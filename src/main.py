import html
import time
from collections import defaultdict
from pathlib import Path

import streamlit as st

from src.chat_manager import (
    add_message,
    create_chat,
    delete_all_chats,
    delete_chat,
    find_chat,
    load_chats,
    rename_chat,
    save_chat,
    search_chats,
    update_message_feedback,
)

from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)

from src.langchain_helper import get_qa_stream


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Support",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
<style>

:root {
    --accent: #e85b5b;
    --accent-dark: #d94b4b;
    --accent-soft: #fff4f4;

    --text: #202020;
    --muted: #777777;
    --subtle: #999999;

    --border: #e7e7e7;
    --border-dark: #d8d8d8;

    --surface: #fafafa;
    --surface-2: #f6f6f6;
    --white: #ffffff;
}

/* ============================================================
   APPLICATION
   ============================================================ */

.stApp {
    background: var(--white);
    color: var(--text);
}

.block-container {
    max-width: 1120px;
    padding-top: 0;
    padding-bottom: 120px;
}


/* ============================================================
   HEADER
   ============================================================ */

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stDecoration"] {
    display: none;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebarContent"] {
    padding: 18px 12px 20px;
}

.sidebar-brand {
    padding: 3px 7px 19px;
}

.sidebar-brand-row {
    display: flex;
    align-items: center;
}

.sidebar-logo {
    width: 31px;
    height: 31px;
    border-radius: 9px;
    background: var(--accent);
    color: white;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 10px;
    font-weight: 800;

    margin-right: 9px;
}

.sidebar-brand-name {
    color: var(--text);
    font-size: 17px;
    font-weight: 750;
    letter-spacing: -0.2px;
}

.sidebar-brand-subtitle {
    color: var(--subtle);
    font-size: 10px;
    margin-top: 5px;
    margin-left: 1px;
}

.sidebar-section-label {
    color: #999999;
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 0.12em;

    margin: 18px 7px 7px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 39px;
    border-radius: 9px;
    font-size: 12px;
}

.sidebar-empty {
    color: #999999;
    font-size: 11px;
    padding: 9px 7px;
}

.sidebar-chat-active button {
    background: #f1f1f1 !important;
}


/* ============================================================
   TOP NAVIGATION
   ============================================================ */

.top-navigation {
    height: 58px;

    display: flex;
    align-items: center;

    border-bottom: 1px solid #eeeeee;
}

.top-navigation-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 700;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.top-navigation-subtitle {
    color: #9a9a9a;
    font-size: 9px;
    margin-top: 2px;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-state {
    max-width: 720px;
    margin: 135px auto 0;

    text-align: center;
}

.empty-state-mark {
    width: 44px;
    height: 44px;

    margin: 0 auto 17px;

    border-radius: 13px;

    background: var(--accent-soft);
    border: 1px solid #ffe0e0;

    color: var(--accent);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 21px;
    font-weight: 700;
}

.empty-state-title {
    color: var(--text);

    font-size: 26px;
    line-height: 1.2;

    font-weight: 740;
    letter-spacing: -0.7px;
}

.empty-state-description {
    color: #858585;

    font-size: 12px;
    line-height: 1.55;

    max-width: 500px;

    margin: 9px auto 0;
}


/* ============================================================
   SUGGESTIONS
   ============================================================ */

.suggestion-area {
    max-width: 720px;
    margin: 30px auto 0;
}

.suggestion-label {
    color: #8d8d8d;
    font-size: 10px;
    font-weight: 650;
    margin: 0 0 7px 2px;
}

.suggestion-area .stButton > button {
    background: white !important;
    border: 1px solid #e5e5e5 !important;

    color: #3b3b3b !important;

    min-height: 48px;

    border-radius: 10px !important;

    font-size: 11px !important;

    transition:
        border-color 0.15s ease,
        background 0.15s ease;
}

.suggestion-area .stButton > button:hover {
    background: #fafafa !important;
    border-color: #cccccc !important;
}


/* ============================================================
   ATTACHMENT PREVIEW
   ============================================================ */

.attachment-strip {
    max-width: 760px;

    margin: 20px auto 4px;

    display: flex;
    flex-wrap: wrap;
    gap: 7px;
}

.attachment-card {
    background: #fafafa;

    border: 1px solid var(--border);

    border-radius: 10px;

    padding: 7px 10px;

    min-width: 155px;
}

.attachment-name {
    color: #333333;

    font-size: 10px;
    font-weight: 650;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    max-width: 190px;
}

.attachment-type {
    color: #999999;
    font-size: 9px;
    margin-top: 2px;
}


/* ============================================================
   FILE MANAGEMENT
   ============================================================ */

.file-list-card {
    background: #fafafa;

    border: 1px solid var(--border);

    border-radius: 11px;

    padding: 10px 12px;

    margin-bottom: 7px;
}

.file-list-name {
    font-size: 11px;
    font-weight: 650;
}

.file-list-meta {
    color: #929292;
    font-size: 9px;
    margin-top: 3px;
}


/* ============================================================
   SOURCES
   ============================================================ */

.source-wrapper {
    margin-top: 8px;
}

.source-group {
    background: #fafafa;

    border: 1px solid var(--border);

    border-radius: 10px;

    padding: 9px 11px;

    margin: 5px 0;
}

.source-group-name {
    color: #333333;

    font-size: 11px;
    font-weight: 650;
}

.source-group-meta {
    color: #929292;

    font-size: 9px;

    margin-top: 3px;
}


/* ============================================================
   MESSAGE ACTIONS
   ============================================================ */

.message-actions {
    margin-top: 2px;
}

.message-actions .stButton > button {
    min-width: 32px !important;
    min-height: 29px !important;

    padding: 2px 7px !important;

    border: none !important;
    background: transparent !important;

    color: #929292 !important;

    font-size: 12px !important;
}

.message-actions .stButton > button:hover {
    background: #f5f5f5 !important;
    color: #555555 !important;
}


/* ============================================================
   SETTINGS
   ============================================================ */

.settings-title {
    color: var(--text);

    font-size: 15px;
    font-weight: 720;

    margin-bottom: 12px;
}

.settings-description {
    color: #888888;
    font-size: 10px;
    line-height: 1.5;

    margin-bottom: 12px;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    border-top: none !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 13px !important;
}

[data-testid="stChatInput"] button {
    border-radius: 9px !important;
}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {
    padding-top: 10px;
    padding-bottom: 10px;
}

[data-testid="stChatMessageContent"] {
    font-size: 13px;
    line-height: 1.65;
}


/* ============================================================
   SMALL SCREENS
   ============================================================ */

@media (max-width: 800px) {

    .block-container {
        padding-left: 14px;
        padding-right: 14px;
    }

    .empty-state {
        margin-top: 90px;
    }

    .empty-state-title {
        font-size: 23px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_chat_id" not in st.session_state:

    existing_chats = load_chats()

    if existing_chats:

        st.session_state.current_chat_id = (
            existing_chats[0]["id"]
        )

    else:

        first_chat = create_chat()
        save_chat(first_chat)

        st.session_state.current_chat_id = (
            first_chat["id"]
        )


if "search_text" not in st.session_state:
    st.session_state.search_text = ""


if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


if "editing_index" not in st.session_state:
    st.session_state.editing_index = None


if "attachment_signature" not in st.session_state:
    st.session_state.attachment_signature = ""


if "show_sources" not in st.session_state:
    st.session_state.show_sources = True


if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False


# ============================================================
# CHAT HELPERS
# ============================================================

def get_current_chat():
    chats = load_chats()

    chat = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if chat is not None:
        return chat

    new_chat = create_chat()
    save_chat(new_chat)

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    return new_chat


def create_new_chat():
    new_chat = create_chat()

    save_chat(new_chat)

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    st.session_state.pending_question = None
    st.session_state.editing_index = None
    st.session_state.attachment_signature = ""
    st.session_state.show_analytics = False

    st.rerun()


def trim_chat(chat, index):
    if index < 0:
        return

    chat["messages"] = (
        chat.get("messages", [])[:index]
    )

    save_chat(chat)


# ============================================================
# SOURCE HELPERS
# ============================================================

def get_source_parts(source):

    if isinstance(source, dict):

        content = source.get(
            "page_content",
            source.get(
                "content",
                "",
            ),
        )

        metadata = source.get(
            "metadata",
            {},
        )

    else:

        content = getattr(
            source,
            "page_content",
            str(source),
        )

        metadata = getattr(
            source,
            "metadata",
            {},
        )

    if not isinstance(metadata, dict):
        metadata = {}

    return (
        str(content or ""),
        metadata,
    )


def identify_source(source):

    content, metadata = (
        get_source_parts(source)
    )

    source_type = (
        metadata.get("source_type")
        or metadata.get("retrieval_source")
    )

    if source_type == "conversation_file":

        filename = (
            metadata.get("source_file")
            or metadata.get("file_name")
            or metadata.get("filename")
            or "Attached file"
        )

        return (
            "file",
            Path(
                str(filename)
            ).name,
            content,
            metadata,
        )

    return (
        "global",
        "Knowledge Base",
        content,
        metadata,
    )


def render_sources(sources):

    if not sources:
        return

    if not st.session_state.show_sources:
        return

    groups = defaultdict(list)

    for source in sources:

        (
            kind,
            name,
            content,
            metadata,
        ) = identify_source(source)

        groups[
            (
                kind,
                name,
            )
        ].append(
            (
                content,
                metadata,
            )
        )

    source_count = len(groups)

    source_word = (
        "source"
        if source_count == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {source_count} {source_word}"
    ):

        for group_key, items in groups.items():

            kind, name = group_key

            if kind == "file":

                icon = "📄"
                origin = "Attached file"

            else:

                icon = "◉"
                origin = "Knowledge Base"

            section_word = (
                "section"
                if len(items) == 1
                else "sections"
            )

            safe_name = html.escape(
                str(name)
            )

            st.markdown(
                '<div class="source-group">'
                '<div class="source-group-name">'
                f'{icon} {safe_name}'
                '</div>'
                '<div class="source-group-meta">'
                f'{len(items)} relevant '
                f'{section_word} · {origin}'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

            for number, (
                content,
                metadata,
            ) in enumerate(
                items,
                1,
            ):

                location = (
                    metadata.get("section")
                    or metadata.get("location")
                    or f"Relevant section {number}"
                )

                with st.expander(
                    str(location)
                ):

                    st.write(
                        content
                    )


# ============================================================
# EXPORT
# ============================================================

def export_markdown(chat):

    title = str(
        chat.get(
            "title",
            "Conversation",
        )
    )

    lines = [
        f"# {title}",
        "",
    ]

    for message in chat.get(
        "messages",
        [],
    ):

        role = str(
            message.get(
                "role",
                "assistant",
            )
        ).capitalize()

        content = str(
            message.get(
                "content",
                "",
            )
        )

        lines.extend(
            [
                f"## {role}",
                "",
                content,
                "",
            ]
        )

    return "\n".join(lines)


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):

    question = str(
        question or ""
    ).strip()

    if not question:
        return

    chat = get_current_chat()

    history = list(
        chat.get(
            "messages",
            [],
        )
    )

    add_message(
        chat,
        "user",
        question,
    )

    started_at = time.time()

    try:

        stream, sources = get_qa_stream(
            question,
            chat_history=history,
            chat_id=chat["id"],
        )

        with st.chat_message(
            "assistant"
        ):

            answer = st.write_stream(
                stream
            )

        if not isinstance(
            answer,
            str,
        ):

            answer = "".join(
                str(part)
                for part in answer
            )

        answer = answer.strip()

        response_time = (
            time.time()
            - started_at
        )

        refreshed_chat = find_chat(
            load_chats(),
            chat["id"],
        )

        if refreshed_chat is None:

            st.error(
                "The conversation could not be saved."
            )

            return

        add_message(
            refreshed_chat,
            "assistant",
            answer,
            sources=sources,
            response_time=response_time,
        )

        st.rerun()

    except Exception as error:

        error_text = str(error)
        lowered = error_text.lower()

        if (
            "429" in lowered
            or "resource_exhausted" in lowered
            or "quota" in lowered
        ):

            st.error(
                "The AI service usage limit has been reached. Please try again later."
            )

        else:

            st.error(
                "The AI service is temporarily unavailable."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    error_text
                )


# ============================================================
# CURRENT CHAT
# ============================================================

current_chat = get_current_chat()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-row">

                <div class="sidebar-logo">
                    AI
                </div>

                <div class="sidebar-brand-name">
                    AI Support
                </div>

            </div>

            <div class="sidebar-brand-subtitle">
                Intelligent customer support
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New chat",
        type="primary",
        use_container_width=True,
        key="new_chat_button",
    ):

        create_new_chat()

    st.markdown(
        '<div class="sidebar-section-label">'
        'SEARCH'
        '</div>',
        unsafe_allow_html=True,
    )

    search_value = st.text_input(
        "Search",
        value=st.session_state.search_text,
        placeholder="Search conversations...",
        label_visibility="collapsed",
        key="conversation_search",
    )

    st.session_state.search_text = (
        search_value
    )

    all_chats = load_chats()

    if search_value.strip():

        visible_chats = search_chats(
            all_chats,
            search_value,
        )

    else:

        visible_chats = all_chats

    st.markdown(
        '<div class="sidebar-section-label">'
        'RECENT'
        '</div>',
        unsafe_allow_html=True,
    )

    if not visible_chats:

        st.markdown(
            '<div class="sidebar-empty">'
            'No conversations found.'
            '</div>',
            unsafe_allow_html=True,
        )

    for item in visible_chats:

        chat_id = item["id"]

        title = str(
            item.get(
                "title",
                "New chat",
            )
        )

        if len(title) > 34:
            title = title[:31] + "..."

        is_active = (
            chat_id
            == st.session_state.current_chat_id
        )

        prefix = (
            "● "
            if is_active
            else ""
        )

        if st.button(
            prefix + title,
            key="conversation_" + chat_id,
            use_container_width=True,
        ):

            st.session_state.current_chat_id = (
                chat_id
            )

            st.session_state.pending_question = None
            st.session_state.editing_index = None

            st.rerun()


# ============================================================
# TOP BAR
# ============================================================

top_left, top_right = st.columns(
    [9, 1]
)

with top_left:

    current_title = html.escape(
        str(
            current_chat.get(
                "title",
                "New chat",
            )
        )
    )

    st.markdown(
        '<div class="top-navigation">'
        '<div>'
        f'<div class="top-navigation-title">'
        f'{current_title}'
        '</div>'
        '<div class="top-navigation-subtitle">'
        'Customer Support'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


with top_right:

    if hasattr(
        st,
        "popover",
    ):

        settings_container = st.popover(
            "⚙",
            use_container_width=True,
        )

    else:

        settings_container = st.expander(
            "⚙",
            expanded=False,
        )

    with settings_container:

        st.markdown(
            '<div class="settings-title">'
            'Settings'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="settings-description">'
            'Conversation and application controls.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.session_state.show_sources = (
            st.checkbox(
                "Show sources",
                value=st.session_state.show_sources,
                key="show_sources_setting",
            )
        )

        st.divider()

        st.markdown(
            "Conversation",
        )

        rename_value = st.text_input(
            "Name",
            value=current_chat.get(
                "title",
                "New chat",
            ),
            label_visibility="collapsed",
            key="rename_value",
        )

        if st.button(
            "Rename",
            use_container_width=True,
            key="rename_conversation",
        ):

            if rename_value.strip():

                rename_chat(
                    current_chat,
                    rename_value.strip(),
                )

                st.rerun()

        export_data = export_markdown(
            current_chat
        )

        st.download_button(
            "Export",
            data=export_data,
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
            key="export_conversation",
        )

        st.divider()

        if st.button(
            "Analytics",
            use_container_width=True,
            key="open_analytics",
        ):

            st.session_state.show_analytics = True

            st.rerun()

        st.divider()

        if st.button(
            "Delete conversation",
            use_container_width=True,
            key="delete_conversation",
        ):

            deleted_id = (
                current_chat["id"]
            )

            remaining = delete_chat(
                load_chats(),
                deleted_id,
            )

            delete_all_conversation_files(
                [deleted_id]
            )

            if remaining:

                st.session_state.current_chat_id = (
                    remaining[0]["id"]
                )

            else:

                replacement = create_chat()

                save_chat(
                    replacement
                )

                st.session_state.current_chat_id = (
                    replacement["id"]
                )

            st.session_state.attachment_signature = ""
            st.session_state.editing_index = None

            st.rerun()

        if st.button(
            "Delete all conversations",
            use_container_width=True,
            key="delete_all_conversations",
        ):

            ids = [
                item["id"]
                for item in load_chats()
            ]

            delete_all_chats()

            delete_all_conversation_files(
                ids
            )

            replacement = create_chat()

            save_chat(
                replacement
            )

            st.session_state.current_chat_id = (
                replacement["id"]
            )

            st.session_state.attachment_signature = ""
            st.session_state.editing_index = None

            st.rerun()


# ============================================================
# ANALYTICS
# ============================================================

if st.session_state.show_analytics:

    try:

        from src.analytics import render_analytics

        render_analytics()

        st.divider()

        if st.button(
            "← Return to chat",
            use_container_width=True,
            key="return_from_analytics",
        ):

            st.session_state.show_analytics = False

            st.rerun()

        st.stop()

    except Exception as error:

        st.error(
            "Analytics could not be loaded."
        )

        st.caption(
            str(error)
        )

        if st.button(
            "Return to chat",
            key="return_from_analytics_error",
        ):

            st.session_state.show_analytics = False

            st.rerun()

        st.stop()


# ============================================================
# EXISTING ATTACHMENTS
# ============================================================

existing_files = list_conversation_files(
    current_chat["id"]
)

if existing_files:

    attachment_html = (
        '<div class="attachment-strip">'
    )

    for record in existing_files:

        filename = (
            record.get(
                "original_name"
            )
            or record.get(
                "file_name"
            )
            or record.get(
                "filename"
            )
            or "Attached file"
        )

        suffix = Path(
            str(filename)
        ).suffix.lower()

        extension = (
            suffix.replace(
                ".",
                ""
            ).upper()
            if suffix
            else "FILE"
        )

        attachment_html += (
            '<div class="attachment-card">'
            '<div class="attachment-name">'
            f'📄 {html.escape(str(filename))}'
            '</div>'
            '<div class="attachment-type">'
            f'{extension}'
            '</div>'
            '</div>'
        )

    attachment_html += "</div>"

    st.markdown(
        attachment_html,
        unsafe_allow_html=True,
    )

    with st.expander(
        "Manage attached files"
    ):

        for record in existing_files:

            file_id = record.get(
                "id"
            )

            filename = (
                record.get(
                    "original_name"
                )
                or record.get(
                    "file_name"
                )
                or "Attached file"
            )

            chunk_count = record.get(
                "chunk_count",
                0,
            )

            left, right = st.columns(
                [9, 1]
            )

            with left:

                st.markdown(
                    '<div class="file-list-card">'
                    '<div class="file-list-name">'
                    f'📄 {html.escape(str(filename))}'
                    '</div>'
                    '<div class="file-list-meta">'
                    f'{chunk_count} indexed chunks'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            with right:

                if st.button(
                    "×",
                    key=(
                        "delete_attachment_"
                        + str(file_id)
                    ),
                    help="Remove attachment",
                ):

                    removed = (
                        remove_conversation_file(
                            current_chat["id"],
                            file_id,
                        )
                    )

                    if removed:

                        st.session_state.attachment_signature = ""

                        st.rerun()


# ============================================================
# EMPTY CHAT STATE
# ============================================================

messages = current_chat.get(
    "messages",
    [],
)

if not messages:

    st.markdown(
        """
        <div class="empty-state">

            <div class="empty-state-mark">
                ✦
            </div>

            <div class="empty-state-title">
                AI Support
            </div>

            <div class="empty-state-description">
                Ask a support question or attach a document
                to get answers grounded in your available information.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="suggestion-area">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="suggestion-label">'
        'Start with'
        '</div>',
        unsafe_allow_html=True,
    )

    suggestions = [
        "What information is available?",
        "How do I solve a common issue?",
        "What is the code in this file related to?",
        "What does this document contain?",
    ]

    suggestion_columns = st.columns(
        2
    )

    for index, suggestion in enumerate(
        suggestions
    ):

        with suggestion_columns[
            index % 2
        ]:

            if st.button(
                suggestion,
                key=(
                    "suggestion_"
                    + str(index)
                ),
                use_container_width=True,
            ):

                st.session_state.pending_question = (
                    suggestion
                )

                st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for index, message in enumerate(
    messages
):

    role = message.get(
        "role",
        "assistant",
    )

    content = str(
        message.get(
            "content",
            "",
        )
    )

    with st.chat_message(
        role
    ):

        # ----------------------------------------------------
        # EDIT MODE
        # ----------------------------------------------------

        if (
            role == "user"
            and st.session_state.editing_index
            == index
        ):

            edited_text = st.text_area(
                "Edit message",
                value=content,
                label_visibility="collapsed",
                key=(
                    "editing_message_"
                    + str(index)
                ),
                height=100,
            )

            save_column, cancel_column = (
                st.columns(2)
            )

            with save_column:

                if st.button(
                    "Save & regenerate",
                    type="primary",
                    use_container_width=True,
                    key=(
                        "save_edit_"
                        + str(index)
                    ),
                ):

                    edited_text = (
                        edited_text.strip()
                    )

                    if not edited_text:

                        st.warning(
                            "Message cannot be empty."
                        )

                    else:

                        trim_chat(
                            current_chat,
                            index,
                        )

                        st.session_state.editing_index = None

                        st.session_state.pending_question = (
                            edited_text
                        )

                        st.rerun()

            with cancel_column:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key=(
                        "cancel_edit_"
                        + str(index)
                    ),
                ):

                    st.session_state.editing_index = None

                    st.rerun()

            continue

        # ----------------------------------------------------
        # NORMAL MESSAGE
        # ----------------------------------------------------

        st.markdown(
            content
        )

        # ----------------------------------------------------
        # ASSISTANT ACTIONS
        # ----------------------------------------------------

        if role == "assistant":

            render_sources(
                message.get(
                    "sources",
                    [],
                )
            )

            action_1, action_2, action_3, action_4, action_5 = (
                st.columns(
                    [0.55, 0.55, 0.55, 0.55, 7]
                )
            )

            with action_1:

                if st.button(
                    "👍",
                    key=(
                        "positive_"
                        + str(index)
                    ),
                    help="Helpful",
                ):

                    update_message_feedback(
                        current_chat,
                        index,
                        "positive",
                    )

                    st.rerun()

            with action_2:

                if st.button(
                    "👎",
                    key=(
                        "negative_"
                        + str(index)
                    ),
                    help="Not helpful",
                ):

                    update_message_feedback(
                        current_chat,
                        index,
                        "negative",
                    )

                    st.rerun()

            with action_3:

                if st.button(
                    "↻",
                    key=(
                        "regenerate_"
                        + str(index)
                    ),
                    help="Regenerate response",
                ):

                    if index > 0:

                        previous_message = (
                            current_chat[
                                "messages"
                            ][
                                index - 1
                            ]
                        )

                        if (
                            previous_message.get(
                                "role"
                            )
                            == "user"
                        ):

                            question_to_regenerate = (
                                previous_message.get(
                                    "content",
                                    "",
                                )
                            )

                            trim_chat(
                                current_chat,
                                index,
                            )

                            st.session_state.pending_question = (
                                question_to_regenerate
                            )

                            st.rerun()

            with action_4:

                if st.button(
                    "✎",
                    key=(
                        "edit_question_"
                        + str(index)
                    ),
                    help="Edit question",
                ):

                    if index > 0:

                        previous_message = (
                            current_chat[
                                "messages"
                            ][
                                index - 1
                            ]
                        )

                        if (
                            previous_message.get(
                                "role"
                            )
                            == "user"
                        ):

                            st.session_state.editing_index = (
                                index - 1
                            )

                            st.rerun()

            with action_5:

                response_time = (
                    message.get(
                        "response_time"
                    )
                )

                if response_time is not None:

                    try:

                        st.caption(
                            f"{float(response_time):.2f}s"
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass


# ============================================================
# PENDING QUESTION
# ============================================================

if st.session_state.pending_question:

    pending_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(
        pending_question
    )


# ============================================================
# NATIVE COMPOSER WITH ATTACHMENTS
# ============================================================

chat_input_result = st.chat_input(
    "Ask anything about your support information...",
    accept_file="multiple",
    file_type=[
        "pdf",
        "docx",
        "txt",
        "csv",
        "png",
        "jpg",
        "jpeg",
        "webp",
    ],
    max_uploads=10,
)


# ============================================================
# HANDLE COMPOSER ATTACHMENTS + QUESTION
# ============================================================

if chat_input_result is not None:

    user_text = ""
    composer_files = []

    if isinstance(
        chat_input_result,
        str,
    ):

        user_text = chat_input_result.strip()

    else:

        try:

            user_text = str(
                chat_input_result.text
                or ""
            ).strip()

        except AttributeError:

            user_text = ""

        try:

            composer_files = list(
                chat_input_result.files
                or []
            )

        except AttributeError:

            composer_files = []


    # --------------------------------------------------------
    # ATTACHMENT PROCESSING
    # --------------------------------------------------------

    document_files = []
    image_files = []

    for uploaded_file in composer_files:

        filename = str(
            getattr(
                uploaded_file,
                "name",
                "file",
            )
        )

        suffix = (
            Path(
                filename
            ).suffix.lower()
        )

        if suffix in {
            ".pdf",
            ".docx",
            ".txt",
            ".csv",
        }:

            document_files.append(
                uploaded_file
            )

        elif suffix in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        }:

            image_files.append(
                uploaded_file
            )


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    if document_files:

        try:

            result = add_conversation_files(
                current_chat["id"],
                document_files,
            )

            errors = result.get(
                "errors",
                [],
            )

            for error in errors:

                st.error(
                    str(error)
                )

            added = result.get(
                "added",
                [],
            )

            if added:

                st.session_state.attachment_signature = (
                    get_attachment_signature(
                        document_files
                    )
                )

        except Exception as error:

            st.error(
                "The attached document could not be processed."
            )

            st.caption(
                str(error)
            )


    # --------------------------------------------------------
    # IMAGES
    # --------------------------------------------------------

    if image_files:

        st.warning(
            "Image attachments are available in the composer, "
            "but image understanding is not yet connected to "
            "the current RAG pipeline."
        )

        image_names = [
            str(
                getattr(
                    image,
                    "name",
                    "image",
                )
            )
            for image in image_files
        ]

        st.caption(
            "Selected images: "
            + ", ".join(
                image_names
            )
        )


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    if user_text:

        process_question(
            user_text
        )

    elif document_files:

        st.rerun()