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
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)

from src.langchain_helper import (
    create_vector_db,
    get_qa_stream,
)


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
# CSS
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
    max-width: 1100px;
    padding-top: 0.5rem;
    padding-bottom: 120px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fafafa;
    border-right: 1px solid #e6e6e6;
}

[data-testid="stSidebarContent"] {
    padding: 16px 12px 75px 12px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 38px;
    border-radius: 9px;
    font-size: 13px;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #d7d7d7;
}

[data-testid="stSidebar"] input {
    border-radius: 9px;
    font-size: 13px;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #171717;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.2;
}

.sidebar-logo {
    font-size: 21px;
    line-height: 1;
}

.sidebar-caption {
    color: #888888;
    font-size: 11px;
    margin-top: 5px;
    margin-left: 30px;
    margin-bottom: 16px;
}

.sidebar-section {
    color: #777777;
    font-size: 11px;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.35px;
    margin-top: 18px;
    margin-bottom: 8px;
}

.sidebar-search-button button {
    font-size: 19px !important;
    min-height: 34px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
}

.sidebar-search-button button:hover {
    background: #eeeeee !important;
}


/* =========================================================
   MAIN HEADER
   ========================================================= */

.main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 2px 8px 2px;
}

.main-header-title {
    font-size: 15px;
    font-weight: 650;
    color: #252525;
}

.main-header-subtitle {
    font-size: 11px;
    color: #999999;
    margin-top: 2px;
}


# ============================================================
# HOME SCREEN
# ============================================================

if not chat.get("messages"):

    st.markdown(
        "<div style='height: 55px;'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:64px;
            line-height:1;
            margin-bottom:18px;
        ">
            ✦
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h1 style="
            text-align:center;
            font-size:40px;
            font-weight:750;
            letter-spacing:-1px;
            margin:0 0 12px 0;
            color:#202020;
        ">
            🤖 AI Customer Service Assistant
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            font-size:17px;
            color:#666666;
            line-height:1.6;
            margin:0 auto;
            max-width:700px;
        ">
            Ask questions and get reliable answers from our knowledge base.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='height:28px;'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <h2 style="
            text-align:center;
            font-size:25px;
            font-weight:650;
            margin:0 0 8px 0;
            color:#292929;
        ">
            {st.session_state.greeting}
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            font-size:15px;
            color:#777777;
            line-height:1.6;
            margin:0 auto;
            max-width:680px;
        ">
            I'm ready whenever you are. Ask me something,
            describe a customer issue, or attach a document
            and ask me about it.
        </p>
        """,
        unsafe_allow_html=True,
    )


/* =========================================================
   CHAT
   ========================================================= */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
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
   ATTACHMENTS
   ========================================================= */

.attachment-title {
    color: #555555;
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 8px;
}


/* =========================================================
   SOURCES
   ========================================================= */

.source-heading {
    font-size: 13px;
    font-weight: 650;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer-note {
    text-align: center;
    color: #999999;
    font-size: 12px;
    line-height: 1.5;
    margin-top: 22px;
}


/* =========================================================
   USER MENU
   ========================================================= */

.user-menu-label {
    font-size: 13px;
    font-weight: 550;
    color: #333333;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .home-wrapper {
        margin-top: 45px;
    }

    .home-title {
        font-size: 31px;
    }

    .home-description {
        font-size: 15px;
        padding: 0 14px;
    }

    .home-greeting {
        font-size: 22px;
    }

    .home-greeting-text {
        font-size: 14px;
        padding: 0 14px;
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

    chats = load_chats()

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


def truncate_messages(
    chat,
    message_index,
):

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


def source_information(
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
        ) = source_information(
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

    source_word = (
        "source"
        if source_count == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {source_count} {source_word}",
        expanded=False,
    ):

        for group, items in grouped.items():

            kind, name = group

            if kind == "file":

                st.markdown(
                    f"📄 **{name}**"
                )

                section_count = len(
                    items
                )

                section_word = (
                    "section"
                    if section_count == 1
                    else "sections"
                )

                st.caption(
                    f"Attached file · "
                    f"{section_count} relevant "
                    f"{section_word}"
                )

            else:

                st.markdown(
                    "📚 **Knowledge Base**"
                )

                section_count = len(
                    items
                )

                section_word = (
                    "section"
                    if section_count == 1
                    else "sections"
                )

                st.caption(
                    f"{section_count} relevant "
                    f"{section_word}"
                )

            for number, item in enumerate(
                items,
                1,
            ):

                content, metadata = item

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

    title = str(
        chat.get(
            "title",
            "Conversation",
        )
    )

    lines = [
        "# " + title,
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
            "## " + role
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
# STREAM RESPONSE
# ============================================================

def display_stream(
    stream,
):

    if hasattr(
        st,
        "write_stream",
    ):

        result = st.write_stream(
            stream
        )

        if isinstance(
            result,
            str,
        ):

            return result

        return "".join(
            str(part)
            for part in result
        )

    response_parts = []

    response_placeholder = st.empty()

    for chunk in stream:

        text = str(
            chunk
        )

        response_parts.append(
            text
        )

        response_placeholder.markdown(
            "".join(
                response_parts
            )
        )

    return "".join(
        response_parts
    )


# ============================================================
# PROCESS QUESTION
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

            answer = display_stream(
                stream
            )

        answer = str(
            answer or ""
        ).strip()

        elapsed = (
            time.time()
            - start_time
        )

        refreshed_chats = load_chats()

        refreshed_chat = find_chat(
            refreshed_chats,
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
    # BRAND + SEARCH
    # --------------------------------------------------------

    brand_column, search_column = st.columns(
        [7, 1]
    )

    with brand_column:

        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-logo">✦</span>
                <span>AI Support</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with search_column:

        if st.button(
            "⌕",
            key="sidebar_search",
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
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "✎  New chat",
        type="primary",
        use_container_width=True,
        key="sidebar_new_chat",
    ):

        create_new_chat()


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if st.session_state.search_open:

        search_value = st.text_input(
            "Search conversations",
            value=st.session_state.search_text,
            placeholder="Search chats...",
            label_visibility="collapsed",
            key="sidebar_search_input",
        )

        st.session_state.search_text = (
            search_value
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


    chats = load_chats()


    if st.session_state.search_text.strip():

        visible_chats = search_chats(
            chats,
            st.session_state.search_text.strip(),
        )

    else:

        visible_chats = chats


    if not visible_chats:

        st.caption(
            "No conversations yet."
        )


    for sidebar_chat in visible_chats:

        chat_id = sidebar_chat[
            "id"
        ]

        title = str(
            sidebar_chat.get(
                "title",
                "New Chat",
            )
        )

        if len(title) > 34:

            title = (
                title[:31]
                + "..."
            )

        if chat_id == (
            st.session_state.current_chat_id
        ):

            button_label = (
                "● "
                + title
            )

        else:

            button_label = title


        if st.button(
            button_label,
            use_container_width=True,
            key="sidebar_chat_" + chat_id,
        ):

            st.session_state.current_chat_id = (
                chat_id
            )

            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()


    # --------------------------------------------------------
    # BOTTOM USER MENU
    # --------------------------------------------------------

    st.markdown(
        "<br>" * 4,
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
            "### Aayan Shaikh"
        )

        st.caption(
            "AI Support workspace"
        )


        st.divider()


        # ----------------------------------------------------
        # SETTINGS
        # ----------------------------------------------------

        st.markdown(
            "**Settings**"
        )


        st.session_state.show_sources = (
            st.checkbox(
                "Show source information",
                value=st.session_state.show_sources,
                key="settings_show_sources",
            )
        )


        st.divider()


        # ----------------------------------------------------
        # CURRENT CONVERSATION
        # ----------------------------------------------------

        st.markdown(
            "**Current conversation**"
        )


        new_title = st.text_input(
            "Conversation name",
            value=chat.get(
                "title",
                "New Chat",
            ),
            key="settings_conversation_name",
        )


        if st.button(
            "Rename conversation",
            use_container_width=True,
            key="settings_rename",
        ):

            if new_title.strip():

                rename_chat(
                    chat,
                    new_title.strip(),
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
            key="settings_export",
        )


        if st.button(
            "🧹 Clear current chat",
            use_container_width=True,
            key="settings_clear",
        ):

            chat["messages"] = []
            chat["title"] = "New Chat"

            save_chat(
                chat
            )

            st.session_state.pending_question = None
            st.session_state.editing_index = None

            st.rerun()


        st.divider()


        # ----------------------------------------------------
        # KNOWLEDGE BASE
        # ----------------------------------------------------

        st.markdown(
            "**Knowledge base**"
        )


        if st.button(
            "🔄 Update knowledge base",
            use_container_width=True,
            key="settings_update_kb",
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
            key="settings_analytics",
        ):

            st.session_state.show_analytics = True

            st.rerun()


        st.divider()


        # ----------------------------------------------------
        # DELETE CURRENT
        # ----------------------------------------------------

        if st.button(
            "🗑 Delete conversation",
            use_container_width=True,
            key="settings_delete",
        ):

            current_id = chat["id"]

            remaining = delete_chat(
                load_chats(),
                current_id,
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


        # ----------------------------------------------------
        # DELETE ALL
        # ----------------------------------------------------

        if st.button(
            "⚠ Delete all conversations",
            use_container_width=True,
            key="settings_delete_all",
        ):

            delete_all_chats()

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
            "**About**"
        )

        st.caption(
            "AI Customer Service Assistant powered by "
            "Retrieval-Augmented Generation, Gemini, "
            "FAISS and document intelligence."
        )


# ============================================================
# ANALYTICS
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
        """
        <div class="attachment-title">
            📎 Attached files
        </div>
        """,
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
                        "remove_file_"
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

if not chat.get(
    "messages"
):

    st.markdown(
        """
        <div class="home-wrapper">

            <div class="home-logo">
                ✦
            </div>

            <div class="home-title">
                🤖 AI Customer Service Assistant
            </div>

            <div class="home-description">
                Ask questions and get reliable answers
                from our knowledge base.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="home-greeting">
            {st.session_state.greeting}
        </div>

        <div class="home-greeting-text">
            I'm ready whenever you are. Ask me something,
            describe a customer issue, or attach a document
            and ask me about it.
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
                key="edit_message_" + str(index),
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

                        truncate_messages(
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
        # MESSAGE
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


            actions = st.columns(
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

            with actions[0]:

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

            with actions[1]:

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

            with actions[2]:

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

                            truncate_messages(
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

            with actions[3]:

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

            with actions[4]:

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
# CHAT INPUT CAPABILITIES
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
        uploaded_files = []


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

            uploaded_files = list(
                getattr(
                    composer,
                    "files",
                    [],
                )
                or []
            )


        document_files = []
        image_files = []


        for uploaded_file in uploaded_files:

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
        # DOCUMENT ATTACHMENT
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
                        "The document could not be attached."
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

            image_names = []

            for image in image_files:

                image_names.append(
                    str(
                        getattr(
                            image,
                            "name",
                            "image",
                        )
                    )
                )

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
                "The current document retrieval pipeline "
                "supports PDF, DOCX, TXT and CSV files."
            )


        # ----------------------------------------------------
        # TEXT QUESTION
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
        key="fallback_file_uploader",
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