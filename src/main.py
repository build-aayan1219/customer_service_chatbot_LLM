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
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
<style>

:root {
    --accent: #ff6b6b;
    --accent-hover: #ef5b5b;
    --text: #202124;
    --muted: #777777;
    --border: #e7e7e7;
    --soft: #f7f7f7;
}


/* =========================================================
   APPLICATION
   ========================================================= */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.45rem;
    padding-bottom: 110px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebarContent"] {
    padding: 15px 10px 10px 10px;
}

[data-testid="stSidebarUserContent"] {
    padding-bottom: 85px !important;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 38px;
    border-radius: 9px;
    font-size: 13px;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] input {
    border-radius: 9px;
    font-size: 13px;
}


/* Brand */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 3px 3px 0 3px;
}

.sidebar-brand-logo {
    font-size: 24px;
    line-height: 1;
    color: #161616;
}

.sidebar-brand-name {
    font-size: 18px;
    font-weight: 750;
    color: #161616;
}

.sidebar-caption {
    margin: 7px 0 14px 31px;
    color: #8a8a8a;
    font-size: 11px;
}


/* Sections */

.sidebar-section {
    margin: 18px 3px 7px 3px;
    color: #777777;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.45px;
    text-transform: uppercase;
}

.recent-empty {
    padding: 10px 4px;
    color: #999999;
    font-size: 12px;
}


/* Chat rows */

.sidebar-chat-row {
    display: flex;
    align-items: center;
    gap: 3px;
    margin-bottom: 5px;
}

.sidebar-chat-button {
    flex: 1;
    min-width: 0;
}

.sidebar-menu-button {
    width: 42px;
}

.sidebar-menu-button .stButton > button {
    padding-left: 0 !important;
    padding-right: 0 !important;
    font-size: 17px !important;
}


/* Fixed account menu */

[data-testid="stSidebar"] [class*="st-key-account_menu"] {
    position: fixed !important;
    left: 10px !important;
    bottom: 10px !important;
    width: 260px !important;
    z-index: 9999 !important;
    background: #fbfbfb;
    padding-top: 7px;
    border-top: 1px solid var(--border);
}

[data-testid="stSidebar"] [class*="st-key-account_menu"] button {
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 550 !important;
}


/* =========================================================
   MAIN TOP BAR
   ========================================================= */

.chat-topbar {
    display: flex;
    align-items: center;
    min-height: 34px;
    padding: 3px 0 5px;
    border-bottom: 1px solid #eeeeee;
}

.chat-topbar-title {
    font-size: 14px;
    font-weight: 650;
    color: #262626;
}

.chat-topbar-subtitle {
    margin-left: 9px;
    font-size: 11px;
    color: #999999;
}


/* =========================================================
   HOME SCREEN
   ========================================================= */

.home-wrapper {
    max-width: 850px;
    margin: 0 auto;
    text-align: center;
    padding: 62px 20px 45px;
}

.home-logo {
    font-size: 68px;
    line-height: 1;
    margin-bottom: 20px;
    color: #22252b;
}

.home-title {
    font-size: 38px;
    font-weight: 760;
    letter-spacing: -1px;
    line-height: 1.15;
    color: #202124;
    margin-bottom: 12px;
}

.home-subtitle {
    font-size: 18px;
    font-weight: 500;
    line-height: 1.55;
    color: #555555;
}

.home-greeting {
    margin-top: 32px;
    font-size: 30px;
    font-weight: 730;
    color: #202124;
}

.home-message {
    max-width: 720px;
    margin: 10px auto 0;
    font-size: 16px;
    line-height: 1.65;
    color: #707070;
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

[data-testid="stChatInput"] textarea {
    font-size: 14px !important;
}


/* =========================================================
   ATTACHMENTS
   ========================================================= */

.attachment-heading {
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 6px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-footer {
    text-align: center;
    color: #aaaaaa;
    font-size: 10px;
    margin-top: 12px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .home-wrapper {
        padding-top: 40px;
    }

    .home-title {
        font-size: 29px;
    }

    .home-subtitle {
        font-size: 16px;
    }

    .home-greeting {
        font-size: 25px;
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
            "Welcome back 👋",
            "Hey, ready when you are 👋",
            "Good to see you 👋",
            "Hey there, what can we figure out today? 👋",
        ]
    )


# ============================================================
# CHAT HELPERS
# ============================================================

def get_current_chat():

    chats = load_chats()

    current = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if current is not None:

        return current

    if chats:

        st.session_state.current_chat_id = (
            chats[0]["id"]
        )

        return chats[0]

    new_chat = create_chat()

    save_chat(new_chat)

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    return new_chat


def reset_transient_state():

    st.session_state.pending_question = None

    st.session_state.editing_index = None

    st.session_state.attachment_signature = ""

    st.session_state.show_analytics = False


def create_new_chat():

    new_chat = create_chat()

    save_chat(new_chat)

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    st.session_state.search_text = ""

    reset_transient_state()

    st.rerun()


def truncate_chat(
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

    save_chat(chat)


def make_chat_title(question):

    clean = " ".join(
        str(question)
        .strip()
        .split()
    )

    if not clean:

        return "New Chat"

    if len(clean) > 42:

        return clean[:39] + "..."

    return clean


def ensure_chat_title(
    chat,
    question,
):

    title = str(
        chat.get(
            "title",
            "",
        )
    ).strip()

    if (
        not title
        or title.lower() == "new chat"
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
        ) = source_group(
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

    group_count = len(grouped)

    source_label = (
        "source"
        if group_count == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {group_count} {source_label}",
        expanded=False,
    ):

        for (
            kind,
            name,
        ), items in grouped.items():

            icon = (
                "📄"
                if kind == "file"
                else "📚"
            )

            st.markdown(
                f"{icon} **{name}**"
            )

            item_count = len(items)

            section_label = (
                "section"
                if item_count == 1
                else "sections"
            )

            st.caption(
                f"{item_count} relevant {section_label}"
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

        stream, sources = get_qa_stream(
            question,
            chat_history=history,
            chat_id=active_chat["id"],
        )

        with st.chat_message(
            "assistant"
        ):

            placeholder = st.empty()

            parts = []

            for chunk in stream:

                text = str(
                    chunk
                )

                if text:

                    parts.append(
                        text
                    )

                    placeholder.markdown(
                        "".join(
                            parts
                        )
                    )

        answer = "".join(
            parts
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
    # BRAND
    # --------------------------------------------------------

    brand_col, search_icon_col = st.columns(
        [
            8.5,
            1.5,
        ]
    )

    with brand_col:

        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-brand-logo">✦</span>
                <span class="sidebar-brand-name">
                    AI Support
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with search_icon_col:

        st.markdown(
            """
            <div style="
                font-size:18px;
                text-align:center;
                padding-top:3px;
                color:#555;
            ">
                ⌕
            </div>
            """,
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

    search_value = st.text_input(
        "Search conversations",
        value=st.session_state.search_text,
        placeholder="Search chats...",
        label_visibility="collapsed",
        key="sidebar_search",
    )

    st.session_state.search_text = (
        search_value
    )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋  New chat",
        type="primary",
        use_container_width=True,
        key="new_chat_sidebar",
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


    cleaned_chats = []


    for item in visible_chats:

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if not title:

            title = "New Chat"


        if (
            not item.get(
                "messages"
            )
            and title.lower()
            == "new chat"
            and item["id"]
            != st.session_state.current_chat_id
        ):

            continue


        cleaned_chats.append(
            item
        )


    visible_chats = cleaned_chats[
        :12
    ]


    if not visible_chats:

        st.markdown(
            """
            <div class="recent-empty">
                No conversations yet.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # CHAT ROWS
    # --------------------------------------------------------

    for item in visible_chats:

        item_id = str(
            item["id"]
        )

        raw_title = str(
            item.get(
                "title",
                "New Chat",
            )
        ).strip()

        if not raw_title:

            raw_title = "New Chat"


        display_title = raw_title


        if len(display_title) > 34:

            display_title = (
                display_title[:31]
                + "..."
            )


        if (
            item_id
            == str(
                st.session_state.current_chat_id
            )
        ):

            display_title = (
                "● "
                + display_title
            )


        chat_column, menu_column = st.columns(
            [
                8.7,
                1.3,
            ],
            gap="small",
        )


        # ----------------------------------------------------
        # OPEN CHAT
        # ----------------------------------------------------

        with chat_column:

            if st.button(
                display_title,
                use_container_width=True,
                key=(
                    "chat_open_"
                    + item_id
                ),
            ):

                st.session_state.current_chat_id = (
                    item_id
                )

                reset_transient_state()

                st.rerun()


        # ----------------------------------------------------
        # CHAT THREE DOT MENU
        # ----------------------------------------------------

        with menu_column:

            if hasattr(
                st,
                "popover",
            ):

                chat_menu = st.popover(
                    "⋮",
                    use_container_width=True,
                    key=(
                        "chat_menu_"
                        + item_id
                    ),
                )

                with chat_menu:

                    st.markdown(
                        f"**{raw_title}**"
                    )


                    # ----------------------------------------
                    # RENAME
                    # ----------------------------------------

                    new_title = st.text_input(
                        "Rename",
                        value=raw_title,
                        key=(
                            "rename_input_"
                            + item_id
                        ),
                        label_visibility="collapsed",
                    )


                    if st.button(
                        "Rename",
                        use_container_width=True,
                        key=(
                            "rename_btn_"
                            + item_id
                        ),
                    ):

                        clean_title = (
                            new_title.strip()
                        )

                        if clean_title:

                            rename_chat(
                                item,
                                clean_title,
                            )

                            st.rerun()


                    # ----------------------------------------
                    # EXPORT
                    # ----------------------------------------

                    st.download_button(
                        "Export",
                        data=export_markdown(
                            item
                        ),
                        file_name=(
                            "conversation.md"
                        ),
                        mime="text/markdown",
                        use_container_width=True,
                        key=(
                            "export_btn_"
                            + item_id
                        ),
                    )


                    # ----------------------------------------
                    # DELETE
                    # ----------------------------------------

                    if st.button(
                        "Delete",
                        use_container_width=True,
                        key=(
                            "delete_btn_"
                            + item_id
                        ),
                    ):

                        deleted_id = item_id

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


                        reset_transient_state()

                        st.rerun()


            else:

                st.button(
                    "⋮",
                    key=(
                        "chat_menu_fallback_"
                        + item_id
                    ),
                    help="Chat options",
                )


    # --------------------------------------------------------
    # FIXED ACCOUNT MENU
    # --------------------------------------------------------

    if hasattr(
        st,
        "popover",
    ):

        account_menu = st.popover(
            "◉  Aayan Shaikh",
            use_container_width=True,
            key="account_menu",
        )


        with account_menu:

            st.markdown(
                "### Settings"
            )


            # --------------------------------------------
            # SOURCE SETTING
            # --------------------------------------------

            st.session_state.show_sources = (
                st.checkbox(
                    "Show sources",
                    value=st.session_state.show_sources,
                    key="account_show_sources",
                )
            )


            st.divider()


            # --------------------------------------------
            # ANALYTICS
            # --------------------------------------------

            if st.button(
                "Analytics",
                use_container_width=True,
                key="account_analytics",
            ):

                st.session_state.show_analytics = True

                st.rerun()


            # --------------------------------------------
            # CLEAR CURRENT CHAT
            # --------------------------------------------

            if st.button(
                "Clear current chat",
                use_container_width=True,
                key="account_clear",
            ):

                chat["messages"] = []

                chat["title"] = "New Chat"

                save_chat(
                    chat
                )

                reset_transient_state()

                st.rerun()


            # --------------------------------------------
            # DELETE ALL
            # --------------------------------------------

            if st.button(
                "Delete all conversations",
                use_container_width=True,
                key="account_delete_all",
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


                reset_transient_state()

                st.rerun()


            st.divider()


            st.caption(
                "AI Customer Service Assistant"
            )

            st.caption(
                "Gemini · RAG · Document Q&A"
            )


    else:

        if st.button(
            "◉  Aayan Shaikh",
            use_container_width=True,
            key="account_menu_fallback",
        ):

            st.info(
                "Settings are available in newer Streamlit versions."
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
# MAIN TOP BAR
# ============================================================

has_messages = bool(
    chat.get(
        "messages",
        [],
    )
)


if has_messages:

    chat_title = str(
        chat.get(
            "title",
            "Conversation",
        )
    )


    st.markdown(
        f"""
        <div class="chat-topbar">
            <span class="chat-topbar-title">
                {chat_title}
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

if not has_messages:

    greeting = (
        st.session_state.greeting
    )


    st.markdown(
        f"""
        <div class="home-wrapper">

            <div class="home-logo">
                ✦
            </div>

            <div class="home-title">
                🤖 AI Customer Service Assistant
            </div>

            <div class="home-subtitle">
                Ask questions and get reliable answers
                from our knowledge base.
            </div>

            <div class="home-greeting">
                {greeting}
            </div>

            <div class="home-message">
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


                        st.session_state.editing_index = (
                            None
                        )


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

                    st.session_state.editing_index = (
                        None
                    )

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


            # Like

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
                        chat,
                        index,
                        "positive",
                    )

                    st.rerun()


            # Dislike

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
                        chat,
                        index,
                        "negative",
                    )

                    st.rerun()


            # Regenerate

            with action_columns[2]:

                if st.button(
                    "↻",
                    key=(
                        "regen_"
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


            # Edit

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


            # Response time

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


    st.session_state.pending_question = (
        None
    )


    process_question(
        pending_question
    )


# ============================================================
# CHAT INPUT CAPABILITY DETECTION
# ============================================================

chat_input_parameters = (
    inspect.signature(
        st.chat_input
    ).parameters
)


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
        "placeholder":
            "Message AI Support..."
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


        # ----------------------------------------------------
        # TEXT + FILE EXTRACTION
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # CLASSIFY FILES
        # ----------------------------------------------------

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


            if (
                signature
                != previous_signature
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


        if (
            signature
            != previous_signature
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