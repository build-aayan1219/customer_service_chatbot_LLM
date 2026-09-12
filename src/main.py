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
    page_title="AI Customer Service Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   ROOT
   ========================================================= */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.25rem;
    padding-bottom: 105px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid #e5e5e5;
}

[data-testid="stSidebarContent"] {
    padding: 18px 10px 14px 10px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 39px;
    border-radius: 9px;
    border: 1px solid transparent;
    font-size: 13px;
    font-weight: 500;
}

[data-testid="stSidebar"] input {
    border-radius: 9px;
    font-size: 13px;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 3px 0 3px;
}

.sidebar-brand-logo {
    font-size: 23px;
    line-height: 1;
    color: #161616;
}

.sidebar-brand-name {
    font-size: 18px;
    font-weight: 750;
    color: #161616;
}

.sidebar-caption {
    margin: 7px 0 16px 31px;
    color: #8b8b8b;
    font-size: 11px;
}

.sidebar-search-row {
    margin-bottom: 7px;
}

.sidebar-section {
    margin: 18px 3px 7px 3px;
    color: #777777;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.45px;
    text-transform: uppercase;
}

.recent-empty {
    padding: 12px 4px;
    color: #999999;
    font-size: 12px;
}

.sidebar-bottom-space {
    height: 55px;
}


/* =========================================================
   MAIN TOP BAR
   ========================================================= */

.chat-topbar {
    display: flex;
    align-items: center;
    min-height: 34px;
    padding: 2px 0 3px 0;
}

.chat-topbar-title {
    font-size: 14px;
    font-weight: 650;
    color: #262626;
}

.chat-topbar-subtitle {
    font-size: 11px;
    color: #9a9a9a;
    margin-left: 9px;
}


/* =========================================================
   HOME
   ========================================================= */

.home-wrapper {
    max-width: 820px;
    margin: 0 auto;
    text-align: center;
    padding-top: 58px;
    padding-bottom: 35px;
}

.home-logo {
    font-size: 67px;
    line-height: 1;
    margin-bottom: 22px;
    color: #22252b;
}

.home-title {
    font-size: 39px;
    font-weight: 760;
    letter-spacing: -1.25px;
    line-height: 1.15;
    color: #202124;
    margin-bottom: 13px;
}

.home-subtitle {
    font-size: 18px;
    font-weight: 500;
    line-height: 1.55;
    color: #555555;
    margin: 0 auto;
    max-width: 720px;
}

.home-greeting {
    margin-top: 31px;
    font-size: 29px;
    font-weight: 720;
    letter-spacing: -0.5px;
    color: #202124;
}

.home-message {
    margin: 9px auto 0 auto;
    max-width: 700px;
    font-size: 15px;
    line-height: 1.65;
    color: #777777;
}


/* =========================================================
   CHAT MESSAGES
   ========================================================= */

[data-testid="stChatMessage"] {
    padding-top: 7px;
    padding-bottom: 7px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.7;
}

[data-testid="stChatInput"] {
    border-top: none !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 14px !important;
}


/* =========================================================
   SOURCES
   ========================================================= */

.source-heading {
    font-size: 12px;
    font-weight: 650;
}


/* =========================================================
   ATTACHMENTS
   ========================================================= */

.attachment-heading {
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 5px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-footer {
    text-align: center;
    color: #a4a4a4;
    font-size: 10px;
    margin-top: 14px;
    padding-bottom: 8px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .block-container {
        padding-left: 14px;
        padding-right: 14px;
    }

    .home-wrapper {
        padding-top: 35px;
    }

    .home-logo {
        font-size: 52px;
    }

    .home-title {
        font-size: 29px;
    }

    .home-subtitle {
        font-size: 16px;
    }

    .home-greeting {
        font-size: 24px;
    }

    .home-message {
        font-size: 14px;
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
            "Hey Aayan 👋",
            "Welcome back, Aayan 👋",
            "Hey Aayan, ready when you are 👋",
            "Good to see you, Aayan 👋",
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

    messages = chat.get(
        "messages",
        [],
    )

    chat["messages"] = messages[:message_index]

    save_chat(chat)


def make_chat_title(question):

    clean_question = " ".join(
        str(question).strip().split()
    )

    if not clean_question:
        return "New Chat"

    if len(clean_question) > 42:

        return (
            clean_question[:39]
            + "..."
        )

    return clean_question


def ensure_chat_title(chat, question):

    current_title = str(
        chat.get(
            "title",
            "",
        )
    ).strip()

    if (
        not current_title
        or current_title.lower() == "new chat"
    ):

        chat["title"] = make_chat_title(
            question
        )

        save_chat(chat)


# ============================================================
# SOURCE HELPERS
# ============================================================

def normalize_source(source):

    if isinstance(
        source,
        dict,
    ):

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

    if not isinstance(
        metadata,
        dict,
    ):

        metadata = {}

    return (
        str(content or ""),
        metadata,
    )


def source_group(source):

    content, metadata = normalize_source(
        source
    )

    source_type = (
        metadata.get(
            "source_type"
        )
        or metadata.get(
            "retrieval_source"
        )
    )

    if source_type == "conversation_file":

        filename = (
            metadata.get(
                "source_file"
            )
            or metadata.get(
                "file_name"
            )
            or metadata.get(
                "filename"
            )
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

    grouped_sources = defaultdict(list)

    for source in sources:

        (
            kind,
            name,
            content,
            metadata,
        ) = source_group(
            source
        )

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

    total_groups = len(
        grouped_sources
    )

    source_word = (
        "source"
        if total_groups == 1
        else "sources"
    )

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

            section_word = (
                "section"
                if count == 1
                else "sections"
            )

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
                    metadata.get(
                        "section"
                    )
                    or metadata.get(
                        "heading"
                    )
                    or metadata.get(
                        "location"
                    )
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

    return "\n".join(
        lines
    )


# ============================================================
# QUESTION PROCESSING
# ============================================================

def process_question(question):

    question = str(
        question or ""
    ).strip()

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

        with st.chat_message(
            "assistant"
        ):

            answer_placeholder = st.empty()

            answer_parts = []

            for chunk in stream:

                text = str(
                    chunk
                )

                if text:

                    answer_parts.append(
                        text
                    )

                    answer_placeholder.markdown(
                        "".join(
                            answer_parts
                        )
                    )

        answer = "".join(
            answer_parts
        ).strip()

        elapsed = (
            time.time()
            - start_time
        )

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

        error_text = str(
            error
        )

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

            with st.expander(
                "Technical details"
            ):

                st.code(
                    error_text
                )


# ============================================================
# CURRENT CHAT
# ============================================================

chat = get_current_chat()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND + SEARCH BUTTON
    # --------------------------------------------------------

    brand_col, search_col = st.columns(
        [8, 1.5]
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

        if st.button(
            "⌕",
            key="sidebar_search_button",
            help="Search conversations",
        ):

            st.session_state.search_open = (
                not st.session_state.search_open
            )

            if not st.session_state.search_open:

                st.session_state.search_text = ""

            st.rerun()


    st.markdown(
        """
        <div class="sidebar-caption">
            Intelligent customer service assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # SEARCH ONLY WHEN OPEN
    # --------------------------------------------------------

    if st.session_state.search_open:

        search_value = st.text_input(
            "Search conversations",
            value=st.session_state.search_text,
            placeholder="Search chats...",
            label_visibility="collapsed",
            key="conversation_search",
        )

        st.session_state.search_text = search_value


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋  New chat",
        type="primary",
        use_container_width=True,
        key="sidebar_new_chat",
    ):

        create_new_chat()


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


    # Remove empty default chats except current one.
    cleaned_chats = []

    for item in visible_chats:

        messages = item.get(
            "messages",
            [],
        )

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if (
            not messages
            and title.lower() == "new chat"
            and item["id"]
            != st.session_state.current_chat_id
        ):

            continue

        cleaned_chats.append(
            item
        )


    visible_chats = cleaned_chats


    # Show newest/relevant conversations first.
    visible_chats = visible_chats[:9]


    if not visible_chats:

        st.markdown(
            """
            <div class="recent-empty">
                No conversations yet.
            </div>
            """,
            unsafe_allow_html=True,
        )


    for item in visible_chats:

        item_id = str(
            item["id"]
        )

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if not title:

            title = "New Chat"


        if len(title) > 34:

            title = (
                title[:31]
                + "..."
            )


        if (
            item_id
            == str(
                st.session_state.current_chat_id
            )
        ):

            button_text = (
                "● "
                + title
            )

        else:

            button_text = title


        if st.button(
            button_text,
            use_container_width=True,
            key="recent_chat_" + item_id,
        ):

            st.session_state.current_chat_id = (
                item_id
            )

            st.session_state.pending_question = None

            st.session_state.editing_index = None

            st.session_state.attachment_signature = ""

            st.session_state.show_analytics = False

            st.rerun()


    # --------------------------------------------------------
    # BOTTOM USER MENU
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-bottom-space"></div>
        """,
        unsafe_allow_html=True,
    )


    if hasattr(
        st,
        "popover",
    ):

        user_menu = st.popover(
            "◉  Aayan Shaikh",
            use_container_width=True,
        )

    else:

        user_menu = st.expander(
            "◉  Aayan Shaikh",
            expanded=False,
        )


    with user_menu:

        st.markdown(
            "### Settings"
        )


        st.session_state.show_sources = st.checkbox(
            "Show sources",
            value=st.session_state.show_sources,
            key="settings_show_sources",
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


        edited_title = st.text_input(
            "Conversation title",
            value=current_title,
            key="conversation_title_input",
        )


        if st.button(
            "Rename",
            use_container_width=True,
            key="rename_conversation",
        ):

            clean_title = edited_title.strip()

            if clean_title:

                rename_chat(
                    chat,
                    clean_title,
                )

                st.rerun()


        st.download_button(
            "Export conversation",
            data=export_markdown(
                chat
            ),
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
            key="export_conversation",
        )


        if st.button(
            "Analytics",
            use_container_width=True,
            key="open_analytics",
        ):

            st.session_state.show_analytics = True

            st.rerun()


        st.divider()


        if st.button(
            "Clear current chat",
            use_container_width=True,
            key="clear_current_chat",
        ):

            chat["messages"] = []

            chat["title"] = "New Chat"

            save_chat(
                chat
            )

            st.session_state.pending_question = None

            st.session_state.editing_index = None

            st.session_state.attachment_signature = ""

            st.rerun()


        if st.button(
            "Delete conversation",
            use_container_width=True,
            key="delete_current_chat",
        ):

            deleted_id = chat["id"]

            remaining = delete_chat(
                load_chats(),
                deleted_id,
            )

            delete_all_conversation_files(
                [
                    deleted_id
                ]
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

            st.session_state.pending_question = None

            st.session_state.editing_index = None

            st.session_state.attachment_signature = ""

            st.rerun()


        if st.button(
            "Delete all conversations",
            use_container_width=True,
            key="delete_all_conversations",
        ):

            chat_ids = [
                item["id"]
                for item in load_chats()
            ]

            delete_all_chats()

            delete_all_conversation_files(
                chat_ids
            )

            replacement = create_chat()

            save_chat(
                replacement
            )

            st.session_state.current_chat_id = (
                replacement["id"]
            )

            st.session_state.pending_question = None

            st.session_state.editing_index = None

            st.session_state.attachment_signature = ""

            st.rerun()


        st.divider()


        st.caption(
            "AI Customer Service Assistant"
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
            key="analytics_back_button",
        ):

            st.session_state.show_analytics = False

            st.rerun()

        st.stop()

    except Exception as error:

        st.error(
            "Analytics could not be loaded."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(
                str(error)
            )

        if st.button(
            "← Back to conversation",
            key="analytics_error_back_button",
        ):

            st.session_state.show_analytics = False

            st.rerun()

        st.stop()


# ============================================================
# MAIN TOP BAR
# ============================================================

has_messages = bool(
    chat.get(
        "messages",
        [],
    )
)


if has_messages:

    st.markdown(
        f"""
        <div class="chat-topbar">
            <span class="chat-topbar-title">
                {chat.get("title", "Conversation")}
            </span>
            <span class="chat-topbar-subtitle">
                AI Customer Service Assistant
            </span>
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
        """
        <div class="attachment-heading">
            Attached files
        </div>
        """,
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
            record.get(
                "original_name"
            )
            or record.get(
                "file_name"
            )
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
            index
            % number_of_columns
        ]:

            st.info(
                f"📄 {filename}\n\n"
                f"{size_display} · "
                f"{chunk_count} sections"
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


            left_column, right_column = (
                st.columns(
                    [
                        9,
                        1,
                    ]
                )
            )


            with left_column:

                st.write(
                    "📄 "
                    + filename
                )


            with right_column:

                if st.button(
                    "×",
                    key=(
                        "remove_attachment_"
                        + str(file_id)
                    ),
                    help="Remove attachment",
                ):

                    removed = (
                        remove_conversation_file(
                            chat["id"],
                            file_id,
                        )
                    )

                    if removed:

                        st.session_state.attachment_signature = ""

                        st.rerun()


# ============================================================
# HOME SCREEN
# ============================================================

if not has_messages:

    st.markdown(
        """
        <div class="home-wrapper">
            <div class="home-logo">✦</div>
            <div class="home-title">
                🤖 AI Customer Service Assistant
            </div>
            <div class="home-subtitle">
                Ask questions and get reliable answers
                from our knowledge base.
            </div>
            <div class="home-greeting">
                """
        + st.session_state.greeting
        + """
            </div>
            <div class="home-message">
                I'm ready whenever you are. Ask me something,
                describe a customer issue, or attach a document
                and ask me about it.
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
                    "edit_message_"
                    + str(index)
                ),
                height=110,
            )


            save_column, cancel_column = (
                st.columns(
                    2
                )
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

                    clean_text = (
                        edited_text.strip()
                    )

                    if clean_text:

                        truncate_chat(
                            chat,
                            index,
                        )

                        st.session_state.editing_index = None

                        st.session_state.pending_question = (
                            clean_text
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Message cannot be empty."
                        )


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
                    key=(
                        "message_like_"
                        + str(index)
                    ),
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
                    key=(
                        "message_dislike_"
                        + str(index)
                    ),
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
                    key=(
                        "message_regenerate_"
                        + str(index)
                    ),
                    help="Regenerate response",
                ):

                    if index > 0:

                        previous_message = (
                            chat[
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

                            previous_question = (
                                previous_message.get(
                                    "content",
                                    "",
                                )
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
                    key=(
                        "message_edit_"
                        + str(index)
                    ),
                    help="Edit question",
                ):

                    if index > 0:

                        previous_message = (
                            chat[
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
# STREAMLIT CHAT INPUT CAPABILITIES
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
# MODERN COMPOSER
# ============================================================

if supports_accept_file:

    chat_input_kwargs = {
        "placeholder": "Message AI Support..."
    }


    if supports_max_uploads:

        chat_input_kwargs[
            "accept_file"
        ] = "multiple"

        chat_input_kwargs[
            "max_uploads"
        ] = 10

    else:

        chat_input_kwargs[
            "accept_file"
        ] = True


    if supports_file_type:

        chat_input_kwargs[
            "file_type"
        ] = [
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

            composer_text = (
                composer.strip()
            )

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
                Path(
                    filename
                )
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
        # DOCUMENT PROCESSING
        # ----------------------------------------------------

        if document_files:

            try:

                signature = (
                    get_attachment_signature(
                        document_files
                    )
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

                    result = (
                        add_conversation_files(
                            chat["id"],
                            document_files,
                        )
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
        # IMAGE ATTACHMENT
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
                + ", ".join(
                    image_names
                )
            )


            st.caption(
                "The current document RAG pipeline supports "
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
# FALLBACK COMPOSER
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

            signature = (
                get_attachment_signature(
                    fallback_files
                )
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

                result = (
                    add_conversation_files(
                        chat["id"],
                        fallback_files,
                    )
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