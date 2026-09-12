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
    set_chat_archived,
    set_chat_pinned,
    update_message_feedback,
)

from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)

from src.langchain_helper import (
    create_vector_db,
    get_qa_stream,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Customer Service Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1080px;
    padding-top: 0.8rem;
    padding-bottom: 120px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fafafa;
    border-right: 1px solid #e7e7e7;
}

[data-testid="stSidebarContent"] {
    padding: 16px 12px 82px 12px;
}

[data-testid="stSidebar"] .stButton > button {
    border-radius: 9px;
    min-height: 38px;
    font-size: 13px;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #d8d8d8;
}

[data-testid="stSidebar"] input {
    border-radius: 9px;
    font-size: 13px;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 18px;
    font-weight: 700;
    color: #171717;
    padding: 3px 3px 2px 3px;
}

.sidebar-brand-icon {
    font-size: 19px;
}

.sidebar-caption {
    color: #858585;
    font-size: 11px;
    margin: 2px 0 15px 3px;
}

.sidebar-section-title {
    color: #737373;
    font-size: 11px;
    font-weight: 600;
    margin: 18px 3px 8px 3px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.sidebar-search-row {
    margin-top: 2px;
    margin-bottom: 4px;
}


/* =========================================================
   MAIN HEADER
   ========================================================= */

.main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 2px 12px 2px;
}

.main-header-title {
    font-size: 15px;
    font-weight: 650;
    color: #222222;
}

.main-header-subtitle {
    font-size: 10px;
    color: #999999;
    margin-top: 2px;
}


/* =========================================================
   ORIGINAL-STYLE APP INTRO
   ========================================================= */

.app-intro {
    text-align: center;
    margin-top: 75px;
    margin-bottom: 25px;
}

.app-logo {
    font-size: 52px;
    line-height: 1;
    margin-bottom: 13px;
}

.app-title {
    font-size: 32px;
    font-weight: 750;
    color: #202020;
    letter-spacing: -0.7px;
    margin-bottom: 8px;
}

.app-description {
    font-size: 14px;
    color: #7d7d7d;
    max-width: 610px;
    margin: 0 auto;
    line-height: 1.6;
}


/* =========================================================
   GREETING
   ========================================================= */

.greeting {
    text-align: center;
    font-size: 19px;
    font-weight: 600;
    color: #303030;
    margin-top: 18px;
    margin-bottom: 8px;
}

.greeting-subtitle {
    text-align: center;
    color: #999999;
    font-size: 12px;
    margin-bottom: 25px;
}


/* =========================================================
   ATTACHMENT DISPLAY
   ========================================================= */

.attachment-heading {
    font-size: 12px;
    font-weight: 600;
    color: #555555;
    margin-bottom: 8px;
}


/* =========================================================
   CHAT
   ========================================================= */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.65;
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
    font-size: 13px;
    font-weight: 600;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer-note {
    text-align: center;
    color: #aaaaaa;
    font-size: 10px;
    margin-top: 14px;
}


/* =========================================================
   USER MENU
   ========================================================= */

.user-menu-button {
    margin-top: 18px;
}

[data-testid="stSidebar"] .user-menu-button {
    position: fixed;
    bottom: 10px;
    left: 12px;
    width: 250px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .app-intro {
        margin-top: 45px;
    }

    .app-title {
        font-size: 27px;
    }

    .app-description {
        font-size: 13px;
        padding: 0 15px;
    }

    .greeting {
        font-size: 18px;
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

    chats = load_chats(
        include_archived=False
    )

    if chats:

        st.session_state.current_chat_id = (
            chats[0]["id"]
        )

    else:

        first_chat = create_chat()

        save_chat(
            first_chat
        )

        st.session_state.current_chat_id = (
            first_chat["id"]
        )


if "show_search" not in st.session_state:
    st.session_state.show_search = False


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

    greetings = [
        "Hey Aayan 👋",
        "Hey there 👋",
        "Good to see you, Aayan 👋",
        "Hey Aayan, what are we solving today?",
        "Welcome back, Aayan 👋",
        "Hey there — ready when you are.",
    ]

    st.session_state.greeting = random.choice(
        greetings
    )


# ============================================================
# CHAT HELPERS
# ============================================================

def get_current_chat():

    chats = load_chats(
        include_archived=False
    )

    chat = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if chat is not None:

        return chat

    new_chat = create_chat()

    save_chat(
        new_chat
    )

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    return new_chat


def create_new_chat():

    new_chat = create_chat()

    save_chat(
        new_chat
    )

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    st.session_state.pending_question = None
    st.session_state.editing_index = None
    st.session_state.attachment_signature = ""
    st.session_state.show_analytics = False

    st.rerun()


def trim_chat(
    chat,
    message_index,
):

    if message_index < 0:

        return

    messages = chat.get(
        "messages",
        [],
    )

    chat["messages"] = messages[
        :message_index
    ]

    if not chat["messages"]:

        chat["title"] = "New Chat"

    save_chat(
        chat
    )


# ============================================================
# SOURCE HELPERS
# ============================================================

def normalize_source(
    source,
):

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


def get_source_group(
    source,
):

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


def render_sources(
    sources,
):

    if not sources:
        return

    if not st.session_state.show_sources:
        return

    grouped = defaultdict(list)

    for source in sources:

        (
            kind,
            name,
            content,
            metadata,
        ) = get_source_group(
            source
        )

        grouped[
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

    source_count = len(
        grouped
    )

    if source_count == 1:

        source_label = "source"

    else:

        source_label = "sources"

    with st.expander(
        f"Sources · {source_count} {source_label}",
        expanded=False,
    ):

        for (
            group,
            items,
        ) in grouped.items():

            kind, name = group

            if kind == "file":

                st.markdown(
                    f"📄 **{name}**"
                )

                if len(items) == 1:

                    section_label = "section"

                else:

                    section_label = "sections"

                st.caption(
                    f"Attached file · "
                    f"{len(items)} relevant "
                    f"{section_label}"
                )

            else:

                st.markdown(
                    "📚 **Knowledge Base**"
                )

                if len(items) == 1:

                    section_label = "section"

                else:

                    section_label = "sections"

                st.caption(
                    f"{len(items)} relevant "
                    f"{section_label}"
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

def export_markdown(
    chat,
):

    lines = [
        "# "
        + str(
            chat.get(
                "title",
                "Conversation",
            )
        ),
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

        lines.append(
            "## "
            + role
        )

        lines.append("")

        lines.append(
            content
        )

        lines.append("")

    return "\n".join(
        lines
    )


# ============================================================
# QUESTION PROCESSING
# ============================================================

def process_question(
    question,
):

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

    add_message(
        active_chat,
        "user",
        question,
    )

    start_time = time.time()

    try:

        stream, sources = get_qa_stream(
            question,
            chat_history=history,
            chat_id=active_chat["id"],
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

        elapsed = (
            time.time()
            - start_time
        )

        refreshed_chat = find_chat(
            load_chats(
                include_archived=False
            ),
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
    # BRAND ROW
    # --------------------------------------------------------

    brand_column, search_column = st.columns(
        [7, 1]
    )

    with brand_column:

        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-brand-icon">🤖</span>
                <span>AI Support</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with search_column:

        if st.button(
            "⌕",
            key="sidebar_search_button",
            help="Search conversations",
        ):

            st.session_state.show_search = (
                not st.session_state.show_search
            )

            if not st.session_state.show_search:

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
    # SEARCH
    # --------------------------------------------------------

    if st.session_state.show_search:

        search_value = st.text_input(
            "Search",
            value=st.session_state.search_text,
            placeholder="Search conversations...",
            label_visibility="collapsed",
            key="sidebar_search_input",
        )

        st.session_state.search_text = (
            search_value
        )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "✎  New chat",
        use_container_width=True,
        type="primary",
        key="sidebar_new_chat",
    ):

        create_new_chat()


    # --------------------------------------------------------
    # RECENT CHATS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section-title">'
        "Recent chats"
        "</div>",
        unsafe_allow_html=True,
    )


    chats = load_chats(
        include_archived=False
    )


    if st.session_state.search_text.strip():

        visible_chats = search_chats(
            chats,
            st.session_state.search_text,
        )

    else:

        visible_chats = chats


    if not visible_chats:

        st.caption(
            "No conversations yet."
        )


    for item in visible_chats:

        item_id = item["id"]

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        )

        if len(title) > 35:

            title = (
                title[:32]
                + "..."
            )

        if item_id == (
            st.session_state.current_chat_id
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
            key="chat_" + item_id,
        ):

            st.session_state.current_chat_id = (
                item_id
            )

            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()


    # --------------------------------------------------------
    # USER MENU
    # --------------------------------------------------------

    st.markdown(
        '<div class="user-menu-button"></div>',
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
            "### Account & Settings"
        )

        st.caption(
            "AI Support workspace"
        )


        st.divider()


        # ----------------------------------------------------
        # CHAT SETTINGS
        # ----------------------------------------------------

        st.markdown(
            "**Chat settings**"
        )

        st.session_state.show_sources = (
            st.checkbox(
                "Show source information",
                value=st.session_state.show_sources,
                key="user_menu_sources",
            )
        )


        st.divider()


        # ----------------------------------------------------
        # CONVERSATION
        # ----------------------------------------------------

        st.markdown(
            "**Conversation**"
        )

        rename_value = st.text_input(
            "Conversation name",
            value=chat.get(
                "title",
                "New Chat",
            ),
            key="user_menu_title",
        )


        if st.button(
            "Rename conversation",
            use_container_width=True,
            key="user_menu_rename",
        ):

            if rename_value.strip():

                rename_chat(
                    chat,
                    rename_value.strip(),
                )

                st.rerun()


        if st.button(
            "📌 Pin / Unpin conversation",
            use_container_width=True,
            key="user_menu_pin",
        ):

            set_chat_pinned(
                chat,
                not bool(
                    chat.get(
                        "pinned",
                        False,
                    )
                ),
            )

            st.rerun()


        if st.button(
            "📦 Archive conversation",
            use_container_width=True,
            key="user_menu_archive",
        ):

            set_chat_archived(
                chat,
                True,
            )

            replacement = None

            remaining_chats = load_chats(
                include_archived=False
            )

            for remaining_chat in remaining_chats:

                if remaining_chat["id"] != chat["id"]:

                    replacement = remaining_chat

                    break


            if replacement is None:

                replacement = create_chat()

                save_chat(
                    replacement
                )


            st.session_state.current_chat_id = (
                replacement["id"]
            )

            st.rerun()


        st.download_button(
            "⬇ Export conversation",
            data=export_markdown(
                chat
            ),
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
            key="user_menu_export",
        )


        st.divider()


        # ----------------------------------------------------
        # KNOWLEDGE BASE
        # ----------------------------------------------------

        st.markdown(
            "**Knowledge base**"
        )

        if st.button(
            "🔄 Create / Update Knowledge Base",
            use_container_width=True,
            key="user_menu_kb",
        ):

            with st.spinner(
                "Updating knowledge base..."
            ):

                try:

                    create_vector_db()

                    st.success(
                        "Knowledge base updated successfully."
                    )

                except Exception as error:

                    st.error(
                        "Knowledge base update failed."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(error)
                        )


        st.divider()


        # ----------------------------------------------------
        # ANALYTICS
        # ----------------------------------------------------

        if st.button(
            "📊 Analytics",
            use_container_width=True,
            key="user_menu_analytics",
        ):

            st.session_state.show_analytics = True

            st.rerun()


        st.divider()


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        if st.button(
            "🧹 Clear current chat",
            use_container_width=True,
            key="user_menu_clear",
        ):

            chat["messages"] = []
            chat["title"] = "New Chat"

            save_chat(
                chat
            )

            st.session_state.editing_index = None
            st.session_state.pending_question = None

            st.rerun()


        # ----------------------------------------------------
        # DELETE CURRENT
        # ----------------------------------------------------

        if st.button(
            "🗑 Delete conversation",
            use_container_width=True,
            key="user_menu_delete",
        ):

            deleted_id = chat["id"]

            remaining = delete_chat(
                load_chats(),
                deleted_id,
            )

            delete_all_conversation_files(
                [deleted_id]
            )

            active_remaining = [
                item
                for item in remaining
                if not item.get(
                    "archived",
                    False,
                )
            ]

            if active_remaining:

                st.session_state.current_chat_id = (
                    active_remaining[0]["id"]
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


        # ----------------------------------------------------
        # DELETE ALL
        # ----------------------------------------------------

        if st.button(
            "⚠ Delete all conversations",
            use_container_width=True,
            key="user_menu_delete_all",
        ):

            all_chat_ids = [
                item["id"]
                for item in load_chats()
            ]

            delete_all_chats()

            delete_all_conversation_files(
                all_chat_ids
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


        # ----------------------------------------------------
        # ABOUT
        # ----------------------------------------------------

        st.markdown(
            "**About AI Support**"
        )

        st.caption(
            "An AI-powered customer service assistant "
            "using Retrieval-Augmented Generation (RAG), "
            "Gemini, FAISS and document intelligence."
        )


# ============================================================
# ANALYTICS SCREEN
# ============================================================

if st.session_state.show_analytics:

    try:

        from src.analytics import render_analytics

        render_analytics()

        st.divider()

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

        with st.expander(
            "Technical details"
        ):

            st.code(
                str(error)
            )

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

header_left, header_right = st.columns(
    [10, 1]
)

with header_left:

    st.markdown(
        f"""
        <div class="main-header">
            <div>
                <div class="main-header-title">
                    {chat.get("title", "New Chat")}
                </div>
                <div class="main-header-subtitle">
                    AI Customer Service Assistant
                </div>
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
        '<div class="attachment-heading">'
        "📎 Attached to this conversation"
        "</div>",
        unsafe_allow_html=True,
    )

    file_columns = st.columns(
        min(
            3,
            len(attached_files),
        )
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
            % len(file_columns)
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


            left, right = st.columns(
                [9, 1]
            )


            with left:

                st.write(
                    "📄 "
                    + filename
                )


            with right:

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
# MAIN EMPTY STATE
# ============================================================

if not chat.get(
    "messages"
):

    st.markdown(
        """
        <div class="app-intro">

            <div class="app-logo">
                🤖
            </div>

            <div class="app-title">
                AI Customer Service Assistant
            </div>

            <div class="app-description">
                Ask questions and get reliable answers
                from our knowledge base.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="greeting">
            {st.session_state.greeting}
        </div>

        <div class="greeting-subtitle">
            I'm ready whenever you are. Ask me something,
            or attach a document to get started.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

messages = chat.get(
    "messages",
    []
)


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
        # EDIT USER MESSAGE
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
                key="edit_message_" + str(index),
                height=90,
            )


            save_column, cancel_column = (
                st.columns(2)
            )


            with save_column:

                if st.button(
                    "Save & regenerate",
                    type="primary",
                    use_container_width=True,
                    key="save_edit_" + str(index),
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
                            chat,
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
                    key="cancel_edit_" + str(index),
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


            # ------------------------------------------------
            # LIKE
            # ------------------------------------------------

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


            # ------------------------------------------------
            # DISLIKE
            # ------------------------------------------------

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


            # ------------------------------------------------
            # REGENERATE
            # ------------------------------------------------

            with action_columns[2]:

                if st.button(
                    "↻",
                    key="regenerate_" + str(index),
                    help="Regenerate response",
                ):

                    if index > 0:

                        previous = (
                            chat["messages"][
                                index - 1
                            ]
                        )

                        if (
                            previous.get(
                                "role"
                            )
                            == "user"
                        ):

                            previous_question = (
                                previous.get(
                                    "content",
                                    "",
                                )
                            )

                            trim_chat(
                                chat,
                                index,
                            )

                            st.session_state.pending_question = (
                                previous_question
                            )

                            st.rerun()


            # ------------------------------------------------
            # EDIT
            # ------------------------------------------------

            with action_columns[3]:

                if st.button(
                    "✎",
                    key="edit_" + str(index),
                    help="Edit question",
                ):

                    if index > 0:

                        previous = (
                            chat["messages"][
                                index - 1
                            ]
                        )

                        if (
                            previous.get(
                                "role"
                            )
                            == "user"
                        ):

                            st.session_state.editing_index = (
                                index - 1
                            )

                            st.rerun()


            # ------------------------------------------------
            # RESPONSE TIME
            # ------------------------------------------------

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

    pending_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(
        pending_question
    )


# ============================================================
# CHAT INPUT CAPABILITY
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

    composer_options = {
        "placeholder": "Message AI Support..."
    }


    if supports_max_uploads:

        composer_options[
            "accept_file"
        ] = "multiple"

        composer_options[
            "max_uploads"
        ] = 10

    else:

        composer_options[
            "accept_file"
        ] = True


    if supports_file_type:

        composer_options[
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
        **composer_options
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
        # DOCUMENT FILES
        # ----------------------------------------------------

        if document_files:

            signature = (
                get_attachment_signature(
                    document_files
                )
            )


            if signature != (
                st.session_state.attachment_signature
            ):

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
                        "The document could not be attached."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(error)
                        )


        # ----------------------------------------------------
        # IMAGE FILES
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
                "Image selected successfully."
            )

            st.caption(
                "Selected: "
                + ", ".join(
                    image_names
                )
            )

            st.caption(
                "The current RAG pipeline supports "
                "PDF, DOCX, TXT and CSV document retrieval."
            )


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        if composer_text:

            process_question(
                composer_text
            )


# ============================================================
# OLDER STREAMLIT FALLBACK
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

        signature = (
            get_attachment_signature(
                fallback_files
            )
        )


        if signature != (
            st.session_state.attachment_signature
        ):

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
                    "The document could not be attached."
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
    <div class="footer-note">
        AI Support may occasionally make mistakes.
        Verify important information.
    </div>
    """,
    unsafe_allow_html=True,
)