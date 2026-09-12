import inspect
import random
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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Support",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.2rem;
    padding-bottom: 100px;
}

footer {
    visibility: hidden;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e5e5;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 10px;
}

[data-testid="stSidebarContent"] {
    padding: 10px 10px 12px 10px;
}


/* Brand */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 4px 0 4px;
}

.sidebar-brand-logo {
    font-size: 22px;
    line-height: 1;
    color: #111827;
}

.sidebar-brand-name {
    font-size: 18px;
    line-height: 1;
    font-weight: 750;
    color: #111827;
}

.sidebar-caption {
    margin: 8px 0 16px 29px;
    color: #8b8b8b;
    font-size: 11px;
}


/* Sidebar search icon */

[data-testid="stSidebar"] .search-icon-button button {
    min-height: 36px;
    width: 36px;
    padding: 0;
    border-radius: 9px;
}


/* Search field */

[data-testid="stSidebar"] input {
    border-radius: 9px !important;
    font-size: 13px !important;
}

.sidebar-search {
    margin-top: 4px;
    margin-bottom: 9px;
}


/* New chat */

[data-testid="stSidebar"] .new-chat-button button {
    min-height: 40px;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 600;
}


/* Section title */

.sidebar-section {
    margin: 28px 4px 8px 4px;
    color: #747474;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.55px;
    text-transform: uppercase;
}


/* Chat row */

.chat-row {
    display: flex;
    align-items: center;
    width: 100%;
}


/* Chat buttons */

[data-testid="stSidebar"] .chat-title-button button {
    min-height: 38px;
    border-radius: 9px;
    border: 1px solid transparent;
    background: transparent;
    color: #222222;
    font-size: 13px;
    font-weight: 450;
    text-align: left;
    padding: 0 11px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

[data-testid="stSidebar"] .chat-title-button button:hover {
    background: #f1f1f1;
    border-color: #eeeeee;
}

[data-testid="stSidebar"] .chat-title-button-active button {
    background: #eeeeee;
    border-color: #d8d8d8;
    font-weight: 550;
}


/* Three dot button */

[data-testid="stSidebar"] .chat-menu-button button {
    min-height: 34px;
    width: 34px;
    padding: 0;
    border-radius: 8px;
    border: 1px solid transparent;
    background: transparent;
    color: #555555;
    font-size: 19px;
    line-height: 1;
}

[data-testid="stSidebar"] .chat-menu-button button:hover {
    background: #eeeeee;
    border-color: #dddddd;
}


/* Popover */

[data-testid="stSidebar"] .stPopover {
    width: 100%;
}


/* User menu */

[data-testid="stSidebar"] .user-popover {
    position: fixed;
    left: 10px;
    bottom: 12px;
    width: 286px;
    z-index: 9999;
}

[data-testid="stSidebar"] .user-popover button {
    min-height: 42px;
    border-radius: 9px;
    border: 1px solid #d5d5d5;
    background: #ffffff;
    color: #222222;
    font-size: 13px;
    text-align: left;
}


/* Keep content from being hidden behind user menu */

.sidebar-bottom-padding {
    height: 72px;
}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 40px;
    border-bottom: 1px solid #eeeeee;
    margin-bottom: 15px;
}

.main-header-title {
    font-size: 14px;
    font-weight: 650;
    color: #262626;
}

.main-header-subtitle {
    font-size: 11px;
    color: #999999;
    margin-left: 8px;
}


/* ============================================================
   CLEAN EMPTY CHAT
   ============================================================ */

.empty-chat {
    min-height: 430px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 45px 20px 30px 20px;
}

.empty-chat-logo {
    font-size: 54px;
    line-height: 1;
    margin-bottom: 18px;
    color: #20242a;
}

.empty-chat-title {
    font-size: 30px;
    line-height: 1.2;
    font-weight: 720;
    letter-spacing: -0.7px;
    color: #202124;
}

.empty-chat-subtitle {
    margin-top: 11px;
    max-width: 650px;
    font-size: 15px;
    line-height: 1.6;
    color: #777777;
}

.empty-chat-greeting {
    margin-top: 27px;
    font-size: 22px;
    font-weight: 650;
    color: #202124;
}

.empty-chat-message {
    margin-top: 6px;
    max-width: 620px;
    font-size: 14px;
    line-height: 1.55;
    color: #888888;
}


/* ============================================================
   MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {
    padding-top: 7px;
    padding-bottom: 7px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.7;
}

[data-testid="stChatInput"] textarea {
    font-size: 14px !important;
}


/* ============================================================
   ATTACHMENTS
   ============================================================ */

.attachment-heading {
    font-size: 12px;
    font-weight: 650;
    margin: 5px 0 7px 0;
}

.attachment-card {
    border: 1px solid #e5e5e5;
    border-radius: 10px;
    padding: 10px 12px;
    background: #fafafa;
    font-size: 12px;
}


/* ============================================================
   SOURCES
   ============================================================ */

.source-heading {
    font-size: 12px;
    font-weight: 650;
}


/* ============================================================
   FOOTER
   ============================================================ */

.app-footer {
    text-align: center;
    color: #aaaaaa;
    font-size: 10px;
    margin-top: 10px;
    padding-bottom: 4px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 800px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .empty-chat {
        min-height: 370px;
        padding-top: 30px;
    }

    .empty-chat-logo {
        font-size: 45px;
    }

    .empty-chat-title {
        font-size: 25px;
    }

    .empty-chat-subtitle {
        font-size: 14px;
    }

    .empty-chat-greeting {
        font-size: 20px;
    }

    .empty-chat-message {
        font-size: 13px;
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
    chats = load_chats()

    if chats:
        st.session_state.current_chat_id = chats[0]["id"]
    else:
        new_chat = create_chat()
        save_chat(new_chat)
        st.session_state.current_chat_id = new_chat["id"]


if "search_open" not in st.session_state:
    st.session_state.search_open = False


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


if "greeting" not in st.session_state:
    st.session_state.greeting = random.choice(
        [
            "Hey there 👋",
            "Good to see you 👋",
            "Hey there, ready when you are 👋",
            "Welcome back 👋",
            "Ready when you are 👋",
        ]
    )


# ============================================================
# CHAT HELPERS
# ============================================================

def get_current_chat():
    chats = load_chats()

    current_chat = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if current_chat is not None:
        return current_chat

    if chats:
        st.session_state.current_chat_id = chats[0]["id"]
        return chats[0]

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
    st.session_state.search_open = False
    st.session_state.search_text = ""
    st.session_state.show_analytics = False

    st.rerun()


def truncate_chat(chat, message_index):
    if message_index < 0:
        return

    messages = chat.get("messages", [])
    chat["messages"] = messages[:message_index]

    save_chat(chat)


def make_chat_title(question):
    clean_question = " ".join(
        str(question).strip().split()
    )

    if not clean_question:
        return "New Chat"

    if len(clean_question) > 42:
        return clean_question[:39] + "..."

    return clean_question


def ensure_chat_title(chat, question):
    current_title = str(
        chat.get(
            "title",
            "",
        )
    ).strip()

    if not current_title or current_title.lower() == "new chat":
        chat["title"] = make_chat_title(question)
        save_chat(chat)


# ============================================================
# OPTIONAL CHAT METADATA
# ============================================================

def set_chat_metadata(chat, field_name, value):
    """
    Stores optional UI metadata without requiring the upgraded
    chat manager. If the database manager supports arbitrary
    fields, they are persisted normally.
    """
    try:
        chat[field_name] = value
        save_chat(chat)
        return True
    except Exception:
        return False


def is_chat_pinned(chat):
    return bool(chat.get("pinned", False))


def is_chat_archived(chat):
    return bool(chat.get("archived", False))


def pin_chat(chat):
    current_value = is_chat_pinned(chat)
    return set_chat_metadata(
        chat,
        "pinned",
        not current_value,
    )


def archive_chat(chat):
    current_value = is_chat_archived(chat)
    return set_chat_metadata(
        chat,
        "archived",
        not current_value,
    )


# ============================================================
# SOURCE HELPERS
# ============================================================

def normalize_source(source):
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


def source_group(source):
    content, metadata = normalize_source(source)

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

    grouped_sources = defaultdict(list)

    for source in sources:
        (
            kind,
            name,
            content,
            metadata,
        ) = source_group(source)

        grouped_sources[
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

    total_groups = len(grouped_sources)

    if total_groups == 1:
        source_word = "source"
    else:
        source_word = "sources"

    with st.expander(
        f"Sources · {total_groups} {source_word}",
        expanded=False,
    ):
        for (
            kind,
            name,
        ), items in grouped_sources.items():

            if kind == "file":
                st.markdown(
                    f"📄 **{name}**"
                )
            else:
                st.markdown(
                    "📚 **Knowledge Base**"
                )

            count = len(items)

            if count == 1:
                section_word = "section"
            else:
                section_word = "sections"

            st.caption(
                f"{count} relevant {section_word}"
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
                    or metadata.get("heading")
                    or metadata.get("location")
                )

                if not location:
                    location = f"Relevant section {number}"

                with st.expander(str(location)):
                    st.write(content)


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
# DELETE CURRENT CHAT
# ============================================================

def delete_current_chat(chat):
    deleted_id = chat["id"]

    remaining = delete_chat(
        load_chats(),
        deleted_id,
    )

    try:
        delete_all_conversation_files(
            [deleted_id]
        )
    except Exception:
        pass

    if remaining:
        st.session_state.current_chat_id = remaining[0]["id"]
    else:
        replacement = create_chat()
        save_chat(replacement)
        st.session_state.current_chat_id = replacement["id"]

    st.session_state.pending_question = None
    st.session_state.editing_index = None
    st.session_state.attachment_signature = ""

    st.rerun()


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):
    question = str(question or "").strip()

    if not question:
        return

    active_chat = get_current_chat()

    history = list(
        active_chat.get(
            "messages",
            [],
        )
    )

    ensure_chat_title(
        active_chat,
        question,
    )

    add_message(
        active_chat,
        "user",
        question,
    )

    start_time = time.time()

    try:
        result = get_qa_stream(
            question,
            chat_history=history,
            chat_id=active_chat["id"],
        )

        stream, sources = result

        with st.chat_message("assistant"):
            answer_placeholder = st.empty()
            answer_parts = []

            for chunk in stream:
                text = str(chunk)

                if text:
                    answer_parts.append(text)

                    answer_placeholder.markdown(
                        "".join(answer_parts)
                    )

        answer = "".join(answer_parts).strip()

        elapsed = time.time() - start_time

        refreshed_chat = find_chat(
            load_chats(),
            active_chat["id"],
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
            response_time=elapsed,
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
                "The AI service usage limit has been reached. "
                "Please try again later."
            )
        else:
            st.error(
                "The AI service is temporarily unavailable."
            )

            with st.expander("Technical details"):
                st.code(error_text)


# ============================================================
# CURRENT CHAT
# ============================================================

chat = get_current_chat()

has_messages = bool(
    chat.get(
        "messages",
        [],
    )
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    brand_col, search_col = st.columns(
        [8.5, 1.5],
        gap="small",
    )

    with brand_col:
        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-brand-logo">✦</span>
                <span class="sidebar-brand-name">AI Support</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with search_col:
        st.markdown(
            '<div class="search-icon-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "⌕",
            key="sidebar_search_toggle",
            help="Search conversations",
        ):
            st.session_state.search_open = (
                not st.session_state.search_open
            )

            if not st.session_state.search_open:
                st.session_state.search_text = ""

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    st.markdown(
        """
        <div class="sidebar-caption">
            Intelligent customer service assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if st.session_state.search_open:

        st.markdown(
            '<div class="sidebar-search">',
            unsafe_allow_html=True,
        )

        search_value = st.text_input(
            "Search conversations",
            value=st.session_state.search_text,
            placeholder="Search chats...",
            label_visibility="collapsed",
            key="sidebar_conversation_search",
        )

        st.session_state.search_text = search_value

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    st.markdown(
        '<div class="new-chat-button">',
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
        "</div>",
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # RECENT CHATS
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-section">
            Recent chats
        </div>
        """,
        unsafe_allow_html=True,
    )


    all_chats = load_chats()


    if st.session_state.search_text.strip():

        visible_chats = search_chats(
            all_chats,
            st.session_state.search_text.strip(),
        )

    else:
        visible_chats = all_chats


    cleaned_chats = []

    for item in visible_chats:

        item_messages = item.get(
            "messages",
            [],
        )

        item_title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if (
            not item_messages
            and item_title.lower() == "new chat"
            and item["id"]
            != st.session_state.current_chat_id
        ):
            continue

        if is_chat_archived(item):
            continue

        cleaned_chats.append(item)


    visible_chats = cleaned_chats


    # Pinned chats first
    visible_chats.sort(
        key=lambda item: (
            not is_chat_pinned(item),
            str(
                item.get(
                    "updated_at",
                    "",
                )
            ),
        )
    )


    visible_chats = visible_chats[:12]


    if not visible_chats:

        st.caption(
            "No conversations yet."
        )


    for item in visible_chats:

        item_id = str(
            item["id"]
        )

        item_title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if not item_title:
            item_title = "New Chat"

        display_title = item_title

        if len(display_title) > 31:
            display_title = (
                display_title[:28]
                + "..."
            )


        if is_chat_pinned(item):
            display_title = "📌 " + display_title


        title_column, menu_column = st.columns(
            [8.7, 1.3],
            gap="small",
        )


        with title_column:

            if (
                item_id
                == str(
                    st.session_state.current_chat_id
                )
            ):

                button_text = (
                    "● "
                    + display_title
                )

            else:

                button_text = display_title


            if item_id == str(
                st.session_state.current_chat_id
            ):

                st.markdown(
                    '<div class="chat-title-button chat-title-button-active">',
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    '<div class="chat-title-button">',
                    unsafe_allow_html=True,
                )


            if st.button(
                button_text,
                use_container_width=True,
                key="chat_open_" + item_id,
            ):

                st.session_state.current_chat_id = item_id
                st.session_state.pending_question = None
                st.session_state.editing_index = None
                st.session_state.attachment_signature = ""
                st.session_state.show_analytics = False

                st.rerun()


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        with menu_column:

            st.markdown(
                '<div class="chat-menu-button">',
                unsafe_allow_html=True,
            )


            menu = st.popover(
                "⋯",
                help="Chat options",
                use_container_width=True,
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            with menu:

                st.markdown(
                    f"**{display_title}**"
                )

                st.divider()


                # Share / Export

                st.download_button(
                    "↗  Share",
                    data=export_markdown(item),
                    file_name="conversation.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="share_chat_" + item_id,
                )


                # Rename

                rename_value = st.text_input(
                    "Rename",
                    value=item_title,
                    key="rename_value_" + item_id,
                    label_visibility="collapsed",
                )


                if st.button(
                    "✎  Rename",
                    use_container_width=True,
                    key="rename_chat_" + item_id,
                ):

                    clean_title = rename_value.strip()

                    if clean_title:
                        rename_chat(
                            item,
                            clean_title,
                        )

                        st.rerun()


                st.divider()


                # Pin

                if is_chat_pinned(item):
                    pin_label = "📌  Unpin chat"
                else:
                    pin_label = "📌  Pin chat"


                if st.button(
                    pin_label,
                    use_container_width=True,
                    key="pin_chat_" + item_id,
                ):

                    pin_chat(item)
                    st.rerun()


                # Archive

                if is_chat_archived(item):
                    archive_label = "▣  Unarchive"
                else:
                    archive_label = "▣  Archive"


                if st.button(
                    archive_label,
                    use_container_width=True,
                    key="archive_chat_" + item_id,
                ):

                    archive_chat(item)

                    if item_id == str(
                        st.session_state.current_chat_id
                    ):

                        remaining = [
                            c
                            for c in load_chats()
                            if str(c["id"]) != item_id
                            and not is_chat_archived(c)
                        ]

                        if remaining:
                            st.session_state.current_chat_id = (
                                remaining[0]["id"]
                            )

                    st.rerun()


                # Delete

                if st.button(
                    "🗑  Delete",
                    use_container_width=True,
                    key="delete_chat_" + item_id,
                ):

                    delete_current_chat(item)


    # --------------------------------------------------------
    # USER MENU
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-bottom-padding"></div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="user-popover">',
        unsafe_allow_html=True,
    )


    user_menu = st.popover(
        "◉  Aayan Shaikh",
        use_container_width=True,
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    with user_menu:

        st.markdown(
            "### Settings"
        )


        st.session_state.show_sources = st.checkbox(
            "Show sources",
            value=st.session_state.show_sources,
            key="settings_sources",
        )


        st.divider()


        st.markdown(
            "**Conversation**"
        )


        current_title = str(
            chat.get(
                "title",
                "New Chat",
            )
        )


        settings_title = st.text_input(
            "Conversation title",
            value=current_title,
            key="settings_title",
        )


        if st.button(
            "Rename current chat",
            use_container_width=True,
            key="settings_rename",
        ):

            clean_title = settings_title.strip()

            if clean_title:
                rename_chat(
                    chat,
                    clean_title,
                )

                st.rerun()


        st.download_button(
            "Export current chat",
            data=export_markdown(chat),
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
            key="settings_export",
        )


        if st.button(
            "Analytics",
            use_container_width=True,
            key="settings_analytics",
        ):

            st.session_state.show_analytics = True
            st.rerun()


        st.divider()


        if st.button(
            "Clear current chat",
            use_container_width=True,
            key="settings_clear",
        ):

            chat["messages"] = []
            chat["title"] = "New Chat"

            save_chat(chat)

            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()


        if st.button(
            "Delete current chat",
            use_container_width=True,
            key="settings_delete_current",
        ):

            delete_current_chat(chat)


        if st.button(
            "Delete all conversations",
            use_container_width=True,
            key="settings_delete_all",
        ):

            chat_ids = [
                item["id"]
                for item in load_chats()
            ]

            delete_all_chats()

            try:
                delete_all_conversation_files(
                    chat_ids
                )
            except Exception:
                pass

            replacement = create_chat()
            save_chat(replacement)

            st.session_state.current_chat_id = replacement["id"]
            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()


        st.divider()


        st.caption(
            "AI Support"
        )

        st.caption(
            "Gemini · RAG · Document Q&A"
        )


# ============================================================
# ANALYTICS
# ============================================================

if st.session_state.show_analytics:

    try:

        from src.analytics import render_analytics

        render_analytics()

        if st.button(
            "← Back to conversation",
            key="analytics_back",
        ):

            st.session_state.show_analytics = False
            st.rerun()

        st.stop()

    except Exception as error:

        st.error(
            "Analytics could not be loaded."
        )

        with st.expander("Technical details"):
            st.code(str(error))

        if st.button(
            "← Back to conversation",
            key="analytics_error_back",
        ):

            st.session_state.show_analytics = False
            st.rerun()

        st.stop()


# ============================================================
# MAIN HEADER
# ============================================================

if has_messages:

    title_text = str(
        chat.get(
            "title",
            "Conversation",
        )
    )

    st.markdown(
        f"""
        <div class="main-header">
            <div>
                <span class="main-header-title">
                    {title_text}
                </span>
                <span class="main-header-subtitle">
                    AI Customer Service Assistant
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ATTACHED FILES
# ============================================================

attached_files = list_conversation_files(
    chat["id"]
)


if attached_files:

    st.markdown(
        '<div class="attachment-heading">Attached files</div>',
        unsafe_allow_html=True,
    )


    number_of_columns = min(
        3,
        len(attached_files),
    )


    file_columns = st.columns(
        number_of_columns
    )


    for index, record in enumerate(
        attached_files
    ):

        filename = (
            record.get("original_name")
            or record.get("file_name")
            or "Attached file"
        )

        size_display = record.get(
            "size_display",
            "",
        )

        chunk_count = record.get(
            "chunk_count",
            0,
        )


        with file_columns[
            index % number_of_columns
        ]:

            st.markdown(
                f"""
                <div class="attachment-card">
                    <strong>📄 {filename}</strong><br>
                    <span>
                        {size_display} · {chunk_count} sections
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )


    with st.expander(
        "Manage attachments"
    ):

        for record in attached_files:

            file_id = record.get("id")

            filename = (
                record.get("original_name")
                or record.get("file_name")
                or "Attached file"
            )


            left_column, right_column = st.columns(
                [9, 1]
            )


            with left_column:

                st.write(
                    "📄 "
                    + filename
                )


            with right_column:

                if st.button(
                    "×",
                    key="remove_file_" + str(file_id),
                    help="Remove attachment",
                ):

                    removed = remove_conversation_file(
                        chat["id"],
                        file_id,
                    )

                    if removed:
                        st.session_state.attachment_signature = ""
                        st.rerun()


# ============================================================
# EMPTY CHAT
# ============================================================

if not has_messages:

    st.markdown(
        f"""
        <div class="empty-chat">

            <div class="empty-chat-logo">
                ✦
            </div>

            <div class="empty-chat-title">
                AI Customer Service Assistant
            </div>

            <div class="empty-chat-subtitle">
                Ask questions and get reliable answers
                from your support knowledge base,
                or attach a document and ask about
                its contents.
            </div>

            <div class="empty-chat-greeting">
                {st.session_state.greeting}
            </div>

            <div class="empty-chat-message">
                I'm ready whenever you are.
                Ask me something, describe a customer issue,
                or attach a document and ask me about it.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MESSAGE HISTORY
# ============================================================

for index, message in enumerate(
    chat.get(
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


    with st.chat_message(role):

        # ----------------------------------------------------
        # EDIT MODE
        # ----------------------------------------------------

        if (
            role == "user"
            and st.session_state.editing_index == index
        ):

            edited_text = st.text_area(
                "Edit message",
                value=content,
                label_visibility="collapsed",
                key="edit_message_" + str(index),
                height=110,
            )


            save_column, cancel_column = st.columns(
                2
            )


            with save_column:

                if st.button(
                    "Save & regenerate",
                    type="primary",
                    use_container_width=True,
                    key="save_edit_" + str(index),
                ):

                    clean_text = edited_text.strip()

                    if clean_text:

                        truncate_chat(
                            chat,
                            index,
                        )

                        st.session_state.editing_index = None
                        st.session_state.pending_question = clean_text

                        st.rerun()

                    else:

                        st.warning(
                            "Message cannot be empty."
                        )


            with cancel_column:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key="cancel_edit_" + str(index),
                ):

                    st.session_state.editing_index = None
                    st.rerun()


            continue


        # ----------------------------------------------------
        # NORMAL MESSAGE
        # ----------------------------------------------------

        st.markdown(content)


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


            action_columns = st.columns(
                [
                    0.55,
                    0.55,
                    0.55,
                    0.55,
                    7.8,
                ]
            )


            with action_columns[0]:

                if st.button(
                    "👍",
                    key="like_" + str(index),
                    help="Helpful",
                ):

                    update_message_feedback(
                        chat,
                        index,
                        "positive",
                    )

                    st.rerun()


            with action_columns[1]:

                if st.button(
                    "👎",
                    key="dislike_" + str(index),
                    help="Not helpful",
                ):

                    update_message_feedback(
                        chat,
                        index,
                        "negative",
                    )

                    st.rerun()


            with action_columns[2]:

                if st.button(
                    "↻",
                    key="regenerate_" + str(index),
                    help="Regenerate response",
                ):

                    if index > 0:

                        previous_message = chat[
                            "messages"
                        ][
                            index - 1
                        ]

                        if (
                            previous_message.get(
                                "role"
                            )
                            == "user"
                        ):

                            previous_question = previous_message.get(
                                "content",
                                "",
                            )

                            truncate_chat(
                                chat,
                                index,
                            )

                            st.session_state.pending_question = (
                                previous_question
                            )

                            st.rerun()


            with action_columns[3]:

                if st.button(
                    "✎",
                    key="edit_" + str(index),
                    help="Edit question",
                ):

                    if index > 0:

                        previous_message = chat[
                            "messages"
                        ][
                            index - 1
                        ]

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


            with action_columns[4]:

                response_time = message.get(
                    "response_time"
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
# CHAT INPUT CAPABILITY DETECTION
# ============================================================

chat_input_parameters = inspect.signature(
    st.chat_input
).parameters


supports_accept_file = (
    "accept_file"
    in chat_input_parameters
)

supports_file_type = (
    "file_type"
    in chat_input_parameters
)

supports_max_uploads = (
    "max_uploads"
    in chat_input_parameters
)


# ============================================================
# MODERN CHAT COMPOSER
# ============================================================

if supports_accept_file:

    chat_input_kwargs = {
        "placeholder": "Message AI Support..."
    }


    if supports_max_uploads:

        chat_input_kwargs["accept_file"] = "multiple"
        chat_input_kwargs["max_uploads"] = 10

    else:

        chat_input_kwargs["accept_file"] = True


    if supports_file_type:

        chat_input_kwargs["file_type"] = [
            "pdf",
            "docx",
            "txt",
            "csv",
            "png",
            "jpg",
            "jpeg",
            "webp",
        ]


    composer = st.chat_input(
        **chat_input_kwargs
    )


    if composer is not None:

        composer_text = ""
        composer_files = []


        if isinstance(
            composer,
            str,
        ):

            composer_text = composer.strip()

        else:

            composer_text = str(
                getattr(
                    composer,
                    "text",
                    "",
                )
                or ""
            ).strip()

            composer_files = list(
                getattr(
                    composer,
                    "files",
                    [],
                )
                or []
            )


        document_files = []
        image_files = []


        for uploaded_file in composer_files:

            filename = str(
                getattr(
                    uploaded_file,
                    "name",
                    "",
                )
            )

            extension = (
                Path(filename)
                .suffix
                .lower()
            )


            if extension in {
                ".pdf",
                ".docx",
                ".txt",
                ".csv",
            }:

                document_files.append(
                    uploaded_file
                )

            elif extension in {
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
            }:

                image_files.append(
                    uploaded_file
                )


        # ----------------------------------------------------
        # DOCUMENT ATTACHMENTS
        # ----------------------------------------------------

        if document_files:

            try:

                signature = get_attachment_signature(
                    document_files
                )

            except Exception:

                signature = "|".join(
                    sorted(
                        str(
                            getattr(
                                item,
                                "name",
                                "",
                            )
                        )
                        for item in document_files
                    )
                )


            previous_signature = (
                st.session_state.get(
                    "attachment_signature",
                    "",
                )
            )


            if signature != previous_signature:

                try:

                    result = add_conversation_files(
                        chat["id"],
                        document_files,
                    )


                    st.session_state.attachment_signature = (
                        signature
                    )


                    if isinstance(
                        result,
                        dict,
                    ):

                        errors = result.get(
                            "errors",
                            [],
                        )


                        for error in errors:

                            st.error(
                                str(error)
                            )


                        if result.get(
                            "added"
                        ):

                            st.rerun()


                except Exception as error:

                    st.error(
                        "The attached document could not be processed."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(error)
                        )


        # ----------------------------------------------------
        # IMAGE ATTACHMENTS
        # ----------------------------------------------------

        if image_files:

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


            st.info(
                "Image attachment received."
            )


            st.caption(
                "Selected: "
                + ", ".join(image_names)
            )


            st.caption(
                "The current RAG pipeline processes "
                "PDF, DOCX, TXT and CSV files."
            )


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        if composer_text:

            process_question(
                composer_text
            )


# ============================================================
# FALLBACK CHAT COMPOSER
# ============================================================

else:

    fallback_files = st.file_uploader(
        "Attach documents",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
        ],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="fallback_documents",
    )


    if fallback_files:

        try:

            signature = get_attachment_signature(
                fallback_files
            )

        except Exception:

            signature = "|".join(
                sorted(
                    str(
                        getattr(
                            item,
                            "name",
                            "",
                        )
                    )
                    for item in fallback_files
                )
            )


        previous_signature = (
            st.session_state.get(
                "attachment_signature",
                "",
            )
        )


        if signature != previous_signature:

            try:

                result = add_conversation_files(
                    chat["id"],
                    fallback_files,
                )


                st.session_state.attachment_signature = (
                    signature
                )


                if isinstance(
                    result,
                    dict,
                ):

                    for error in result.get(
                        "errors",
                        [],
                    ):

                        st.error(
                            str(error)
                        )


                    if result.get(
                        "added"
                    ):

                        st.rerun()


            except Exception as error:

                st.error(
                    "The attached document could not be processed."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(
                        str(error)
                    )


    question = st.chat_input(
        "Message AI Support..."
    )


    if question:

        process_question(
            question
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        AI Support may occasionally make mistakes.
        Verify important information.
    </div>
    """,
    unsafe_allow_html=True,
)