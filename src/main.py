import html
import inspect
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
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
<style>

:root {
    --accent: #e45757;
    --accent-light: #fff4f4;
    --border: #e7e7e7;
    --muted: #777777;
    --surface: #fafafa;
    --text: #202020;
}

/* ---------- GLOBAL ---------- */

.stApp {
    background: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 960px;
    padding-top: 0.5rem;
    padding-bottom: 7rem;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: #fafafa;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebarContent"] {
    padding: 16px 12px 20px;
}

.brand {
    padding: 4px 6px 18px;
}

.brand-row {
    display: flex;
    align-items: center;
}

.brand-icon {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: var(--accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    margin-right: 9px;
}

.brand-name {
    font-size: 18px;
    font-weight: 750;
    color: var(--text);
}

.brand-subtitle {
    color: var(--muted);
    font-size: 10px;
    margin-top: 5px;
}

.sidebar-section {
    color: #929292;
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 0.1em;
    margin: 18px 7px 7px;
}

[data-testid="stSidebar"] button {
    border-radius: 9px !important;
    font-size: 12px !important;
}

/* ---------- HEADER ---------- */

.topbar {
    min-height: 54px;
    border-bottom: 1px solid #eeeeee;
    display: flex;
    align-items: center;
}

.chat-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
}

.chat-meta {
    color: #8a8a8a;
    font-size: 10px;
    margin-top: 2px;
}

/* ---------- WELCOME ---------- */

.welcome {
    max-width: 720px;
    margin: 105px auto 42px;
    text-align: center;
}

.welcome-icon {
    width: 58px;
    height: 58px;
    margin: auto auto 18px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-light);
    border: 1px solid #ffdede;
    color: var(--accent);
    font-size: 27px;
    font-weight: 800;
}

.welcome-title {
    font-size: 31px;
    line-height: 1.15;
    letter-spacing: -0.8px;
    font-weight: 760;
    color: var(--text);
}

.welcome-description {
    max-width: 570px;
    margin: 10px auto 0;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.55;
}

.suggestion-label {
    color: #858585;
    font-size: 11px;
    font-weight: 650;
    margin: 0 0 7px 2px;
}

.suggestion button {
    min-height: 52px;
    background: white !important;
    border: 1px solid #e1e1e1 !important;
    border-radius: 11px !important;
    font-size: 12px !important;
    color: #303030 !important;
}

.suggestion button:hover {
    background: #fafafa !important;
    border-color: #cfcfcf !important;
}

/* ---------- FILES ---------- */

.file-panel {
    border: 1px solid var(--border);
    background: #fafafa;
    border-radius: 12px;
    padding: 8px 10px;
    margin: 8px 0;
}

.file-chip {
    display: inline-block;
    background: white;
    border: 1px solid #e4e4e4;
    border-radius: 8px;
    padding: 6px 9px;
    margin: 2px 4px 2px 0;
    font-size: 11px;
}

.file-meta {
    color: #888888;
    margin-left: 5px;
}

.file-context {
    color: #858585;
    font-size: 9px;
    margin-top: 5px;
}

/* ---------- SOURCES ---------- */

.source-group {
    border: 1px solid var(--border);
    background: #fafafa;
    border-radius: 10px;
    padding: 9px 11px;
    margin: 5px 0;
}

.source-name {
    font-size: 12px;
    font-weight: 650;
}

.source-meta {
    color: #858585;
    font-size: 10px;
    margin-top: 3px;
}

/* ---------- SETTINGS ---------- */

.settings-heading {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* ---------- COMPOSER ---------- */

.composer-note {
    text-align: center;
    color: #999999;
    font-size: 9px;
    margin-top: 3px;
}

/* ---------- CHAT ---------- */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_chat_id" not in st.session_state:
    chats = load_chats()

    if chats:
        st.session_state.current_chat_id = chats[0]["id"]
    else:
        first_chat = create_chat()
        save_chat(first_chat)
        st.session_state.current_chat_id = first_chat["id"]

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
# CHAT FUNCTIONS
# ============================================================

def get_current_chat():
    chats = load_chats()

    current = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if current is not None:
        return current

    new_chat = create_chat()
    save_chat(new_chat)

    st.session_state.current_chat_id = new_chat["id"]

    return new_chat


def create_new_chat():
    new_chat = create_chat()
    save_chat(new_chat)

    st.session_state.current_chat_id = new_chat["id"]
    st.session_state.pending_question = None
    st.session_state.editing_index = None
    st.session_state.attachment_signature = ""
    st.session_state.show_analytics = False

    st.rerun()


def trim_chat(chat, index):
    if index < 0:
        return

    chat["messages"] = chat["messages"][:index]
    save_chat(chat)


# ============================================================
# SOURCE FUNCTIONS
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


def get_source_group(source):
    content, metadata = get_source_parts(source)

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
            Path(str(filename)).name,
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
        kind, name, content, metadata = (
            get_source_group(source)
        )

        groups[
            (kind, name)
        ].append(
            (
                content,
                metadata,
            )
        )

    total = len(groups)

    label = (
        "source"
        if total == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {total} {label}"
    ):
        for (
            group,
            items,
        ) in groups.items():

            kind, name = group

            if kind == "file":
                icon = "📄"
                origin = "Attached file"
            else:
                icon = "📚"
                origin = "Knowledge Base"

            section_label = (
                "section"
                if len(items) == 1
                else "sections"
            )

            safe_name = html.escape(
                str(name)
            )

            st.markdown(
                f'<div class="source-group">'
                f'<div class="source-name">'
                f'{icon} {safe_name}'
                f'</div>'
                f'<div class="source-meta">'
                f'{len(items)} relevant '
                f'{section_label} · {origin}'
                f'</div>'
                f'</div>',
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
    lines = [
        f"# {chat.get('title', 'Conversation')}",
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

    start_time = time.time()

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

        elapsed = (
            time.time()
            - start_time
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
            answer.strip(),
            sources=sources,
            response_time=elapsed,
        )

        st.rerun()

    except Exception as error:
        error_text = str(
            error
        )

        lowered = (
            error_text.lower()
        )

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

            st.caption(
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
        <div class="brand">
            <div class="brand-row">
                <div class="brand-icon">AI</div>
                <div class="brand-name">AI Support</div>
            </div>
            <div class="brand-subtitle">
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
        key="sidebar_new_chat",
    ):
        create_new_chat()

    st.markdown(
        '<div class="sidebar-section">SEARCH</div>',
        unsafe_allow_html=True,
    )

    search_text = st.text_input(
        "Search conversations",
        value=st.session_state.search_text,
        placeholder="Search conversations...",
        label_visibility="collapsed",
        key="sidebar_search",
    )

    st.session_state.search_text = search_text

    all_chats = load_chats()

    if search_text.strip():
        visible_chats = search_chats(
            all_chats,
            search_text,
        )
    else:
        visible_chats = all_chats

    st.markdown(
        '<div class="sidebar-section">RECENT CHATS</div>',
        unsafe_allow_html=True,
    )

    if not visible_chats:
        st.markdown(
            '<div class="empty-history">'
            'No conversations found.'
            '</div>',
            unsafe_allow_html=True,
        )

    for item in visible_chats:

        chat_id = item["id"]

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        )

        if len(title) > 34:
            title = title[:31] + "..."

        if (
            chat_id
            == st.session_state.current_chat_id
        ):
            prefix = "● "
        else:
            prefix = ""

        if st.button(
            prefix + title,
            key="chat_" + chat_id,
            use_container_width=True,
        ):
            st.session_state.current_chat_id = (
                chat_id
            )

            st.session_state.show_analytics = (
                False
            )

            st.session_state.editing_index = (
                None
            )

            st.rerun()


# ============================================================
# TOP BAR
# ============================================================

header_left, header_right = st.columns(
    [8, 1]
)

with header_left:

    safe_title = html.escape(
        str(
            current_chat.get(
                "title",
                "New Chat",
            )
        )
    )

    st.markdown(
        '<div class="topbar">'
        '<div>'
        f'<div class="chat-title">'
        f'{safe_title}'
        f'</div>'
        '<div class="chat-meta">'
        'AI Support · Gemini · RAG'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    if hasattr(
        st,
        "popover",
    ):
        settings = st.popover(
            "•••",
            use_container_width=True,
        )
    else:
        settings = st.expander(
            "•••",
            expanded=False,
        )

    with settings:

        st.markdown(
            '<div class="settings-heading">'
            'Settings'
            '</div>',
            unsafe_allow_html=True,
        )

        st.session_state.show_sources = (
            st.checkbox(
                "Show sources",
                value=st.session_state.show_sources,
                key="setting_sources",
            )
        )

        st.caption(
            "Model"
        )

        st.selectbox(
            "Model",
            ["Gemini"],
            label_visibility="collapsed",
            key="setting_model",
        )

        st.divider()

        if st.button(
            "Analytics",
            use_container_width=True,
            key="setting_analytics",
        ):
            st.session_state.show_analytics = True
            st.rerun()

        st.download_button(
            "Export conversation",
            data=export_markdown(
                current_chat
            ),
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
            key="setting_export",
        )

        st.divider()

        rename_value = st.text_input(
            "Conversation name",
            value=current_chat.get(
                "title",
                "New Chat",
            ),
            key="setting_rename",
        )

        if st.button(
            "Rename",
            use_container_width=True,
            key="setting_rename_button",
        ):
            rename_chat(
                current_chat,
                rename_value,
            )
            st.rerun()

        if st.button(
            "Delete conversation",
            use_container_width=True,
            key="setting_delete",
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
                save_chat(replacement)

                st.session_state.current_chat_id = (
                    replacement["id"]
                )

            st.session_state.attachment_signature = ""
            st.session_state.editing_index = None

            st.rerun()

        st.divider()

        if st.button(
            "Delete all conversations",
            use_container_width=True,
            key="setting_delete_all",
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
            save_chat(replacement)

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

        from src.analytics import (
            render_analytics
        )

        render_analytics()

        st.divider()

        if st.button(
            "← Back to conversation",
            use_container_width=True,
            key="analytics_back",
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
            "Back to conversation",
            key="analytics_error_back",
        ):
            st.session_state.show_analytics = False
            st.rerun()

        st.stop()


# ============================================================
# ATTACHED FILES
# ============================================================

attached_files = (
    list_conversation_files(
        current_chat["id"]
    )
)

if attached_files:

    chips = []

    for record in attached_files:

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

        chips.append(
            '<span class="file-chip">'
            f'📄 {html.escape(str(filename))}'
            f'<span class="file-meta">'
            f'{chunk_count} chunks'
            '</span>'
            '</span>'
        )

    st.markdown(
        '<div class="file-panel">'
        + "".join(chips)
        + '<div class="file-context">'
        'Attached files are available to the assistant '
        'in this conversation.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.expander(
        "Manage attachments"
    ):

        for record in attached_files:

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

            size = record.get(
                "size_display",
                "",
            )

            left, right = st.columns(
                [8, 1]
            )

            with left:

                st.write(
                    f"📄 {filename}"
                )

                if size:
                    st.caption(
                        size
                    )

            with right:

                if st.button(
                    "×",
                    key=(
                        "remove_file_"
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
# WELCOME
# ============================================================

if not current_chat.get(
    "messages"
):

    st.markdown(
        """
        <div class="welcome">
            <div class="welcome-icon">✦</div>

            <div class="welcome-title">
                How can I help?
            </div>

            <div class="welcome-description">
                Get answers from your support knowledge base,
                or attach a document and ask questions about it.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="suggestion-label">'
        'Suggestions'
        '</div>',
        unsafe_allow_html=True,
    )

    suggestions = [
        "What information can you help me with?",
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


# ============================================================
# CHAT MESSAGES
# ============================================================

for index, message in enumerate(
    current_chat.get(
        "messages",
        [],
    )
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

        if (
            role == "user"
            and st.session_state.editing_index
            == index
        ):

            edited = st.text_area(
                "Edit message",
                value=content,
                label_visibility="collapsed",
                key=(
                    "edit_box_"
                    + str(index)
                ),
                height=100,
            )

            edit_save, edit_cancel = (
                st.columns(2)
            )

            with edit_save:

                if st.button(
                    "Save & regenerate",
                    type="primary",
                    use_container_width=True,
                    key=(
                        "save_edit_"
                        + str(index)
                    ),
                ):

                    edited = edited.strip()

                    if not edited:

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
                            edited
                        )

                        st.rerun()

            with edit_cancel:

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

        else:

            st.markdown(
                content
            )

            if role == "assistant":

                render_sources(
                    message.get(
                        "sources",
                        [],
                    )
                )

                action_columns = st.columns(
                    [1, 1, 1, 1, 8]
                )

                with action_columns[0]:

                    if st.button(
                        "👍",
                        key=(
                            "like_"
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

                with action_columns[1]:

                    if st.button(
                        "👎",
                        key=(
                            "dislike_"
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

                with action_columns[2]:

                    if st.button(
                        "↻",
                        key=(
                            "regenerate_"
                            + str(index)
                        ),
                        help="Regenerate",
                    ):

                        if index > 0:

                            previous = (
                                current_chat[
                                    "messages"
                                ][
                                    index - 1
                                ]
                            )

                            if previous.get(
                                "role"
                            ) == "user":

                                question = previous.get(
                                    "content",
                                    "",
                                )

                                trim_chat(
                                    current_chat,
                                    index,
                                )

                                st.session_state.pending_question = (
                                    question
                                )

                                st.rerun()

                with action_columns[3]:

                    if st.button(
                        "✎",
                        key=(
                            "edit_"
                            + str(index)
                        ),
                        help="Edit question",
                    ):

                        if index > 0:

                            previous = (
                                current_chat[
                                    "messages"
                                ][
                                    index - 1
                                ]
                            )

                            if previous.get(
                                "role"
                            ) == "user":

                                st.session_state.editing_index = (
                                    index - 1
                                )

                                st.rerun()

                with action_columns[4]:

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

    pending = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(
        pending
    )


# ============================================================
# ATTACHMENT CONTROL
# ============================================================

if hasattr(
    st,
    "popover",
):

    attachment_control = st.popover(
        "＋ Attach",
        use_container_width=False,
    )

else:

    attachment_control = st.expander(
        "＋ Attach",
        expanded=False,
    )

with attachment_control:

    uploaded_files = st.file_uploader(
        "Attach files",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
        ],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="file_uploader",
    )

    st.caption(
        "PDF · DOCX · TXT · CSV"
    )


# ============================================================
# PROCESS ATTACHMENTS
# ============================================================

if uploaded_files:

    signature = (
        get_attachment_signature(
            uploaded_files
        )
    )

    if (
        signature
        != st.session_state.attachment_signature
    ):

        result = (
            add_conversation_files(
                current_chat["id"],
                uploaded_files,
            )
        )

        st.session_state.attachment_signature = (
            signature
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

            st.rerun()


# ============================================================
# COMPOSER
# ============================================================

st.markdown(
    '<div class="composer-note">'
    'Attach files with ＋ Attach'
    '</div>',
    unsafe_allow_html=True,
)

question = st.chat_input(
    "Message AI Support..."
)

if question:

    process_question(
        question
    )