import inspect
import random
import sqlite3
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
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UI_DATABASE_PATH = (
    BASE_DIR / "chat_ui_metadata.db"
)


# ============================================================
# UI METADATA DATABASE
# ============================================================

def initialize_ui_database():
    connection = sqlite3.connect(
        UI_DATABASE_PATH
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_metadata (
            chat_id TEXT PRIMARY KEY,
            pinned INTEGER NOT NULL DEFAULT 0,
            archived INTEGER NOT NULL DEFAULT 0,
            project TEXT NOT NULL DEFAULT ''
        )
        """
    )

    connection.commit()
    connection.close()


def get_chat_metadata(chat_id):
    initialize_ui_database()

    connection = sqlite3.connect(
        UI_DATABASE_PATH
    )

    row = connection.execute(
        """
        SELECT pinned, archived, project
        FROM chat_metadata
        WHERE chat_id = ?
        """,
        (str(chat_id),),
    ).fetchone()

    connection.close()

    if row is None:
        return {
            "pinned": False,
            "archived": False,
            "project": "",
        }

    return {
        "pinned": bool(row[0]),
        "archived": bool(row[1]),
        "project": row[2] or "",
    }


def set_chat_metadata(
    chat_id,
    pinned=None,
    archived=None,
    project=None,
):
    metadata = get_chat_metadata(
        chat_id
    )

    if pinned is not None:
        metadata["pinned"] = bool(
            pinned
        )

    if archived is not None:
        metadata["archived"] = bool(
            archived
        )

    if project is not None:
        metadata["project"] = str(
            project
        )

    initialize_ui_database()

    connection = sqlite3.connect(
        UI_DATABASE_PATH
    )

    connection.execute(
        """
        INSERT INTO chat_metadata (
            chat_id,
            pinned,
            archived,
            project
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(chat_id)
        DO UPDATE SET
            pinned = excluded.pinned,
            archived = excluded.archived,
            project = excluded.project
        """,
        (
            str(chat_id),
            int(metadata["pinned"]),
            int(metadata["archived"]),
            metadata["project"],
        ),
    )

    connection.commit()
    connection.close()


def delete_chat_metadata(chat_ids):
    if not chat_ids:
        return

    initialize_ui_database()

    connection = sqlite3.connect(
        UI_DATABASE_PATH
    )

    connection.executemany(
        """
        DELETE FROM chat_metadata
        WHERE chat_id = ?
        """,
        [
            (str(chat_id),)
            for chat_id in chat_ids
        ],
    )

    connection.commit()
    connection.close()


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   APPLICATION
   ========================================================= */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.35rem;
    padding-bottom: 115px;
}


/* =========================================================
   HIDE STREAMLIT TOP MENU
   ========================================================= */

[data-testid="stToolbar"] {
    display: none !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid #e5e5e5;
}

[data-testid="stSidebarContent"] {
    padding: 17px 12px 90px 12px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 39px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
}

[data-testid="stSidebar"] input {
    border-radius: 10px;
    font-size: 13px;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 4px 4px 0 4px;
}

.sidebar-logo {
    font-size: 25px;
    line-height: 1;
    color: #17191d;
}

.sidebar-name {
    font-size: 18px;
    font-weight: 750;
    color: #17191d;
}

.sidebar-caption {
    margin: 6px 0 16px 34px;
    color: #8a8a8a;
    font-size: 11px;
}


/* =========================================================
   SIDEBAR SECTION
   ========================================================= */

.sidebar-section {
    margin: 22px 4px 8px 4px;
    color: #777777;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}


/* =========================================================
   CHAT ROW
   ========================================================= */

.chat-row [data-testid="column"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
}

.chat-row .stButton > button {
    min-height: 39px;
    text-align: left;
    padding-left: 12px;
    padding-right: 7px;
    border-radius: 9px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

.chat-row .stPopover > button {
    min-height: 39px;
    width: 100%;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #4f4f4f !important;
    font-size: 20px !important;
}

.chat-row .stPopover > button:hover {
    background: #eeeeee !important;
    border-radius: 8px !important;
}


/* =========================================================
   CHAT MENU
   ========================================================= */

.chat-menu-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.chat-menu-danger {
    color: #d64747;
}


/* =========================================================
   FIXED USER MENU
   ========================================================= */

.st-key-user-menu {
    position: fixed !important;
    left: 10px !important;
    bottom: 10px !important;
    width: 292px !important;
    z-index: 999999 !important;
    background: #fbfbfb;
    padding-top: 5px;
}

.st-key-user-menu .stPopover > button {
    min-height: 46px;
    width: 100%;
    border: 1px solid #d8d8d8;
    border-radius: 11px;
    background: #ffffff;
    text-align: left;
    font-size: 13px;
}


/* =========================================================
   MAIN TOP BAR
   ========================================================= */

.main-topbar {
    min-height: 35px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #eeeeee;
    padding-bottom: 8px;
}

.main-topbar-title {
    font-size: 14px;
    font-weight: 650;
    color: #252525;
}

.main-topbar-subtitle {
    font-size: 11px;
    color: #999999;
}


/* =========================================================
   HOME
   ========================================================= */

.home-wrap {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
    padding-top: 78px;
    padding-bottom: 48px;
}

.home-logo {
    font-size: 64px;
    line-height: 1;
    color: #20242b;
    margin-bottom: 21px;
}

.home-title {
    font-size: 40px;
    font-weight: 760;
    letter-spacing: -1.2px;
    line-height: 1.16;
    color: #202124;
}

.home-description {
    max-width: 760px;
    margin: 14px auto 0;
    font-size: 18px;
    font-weight: 450;
    line-height: 1.6;
    color: #555555;
}

.home-greeting {
    margin-top: 40px;
    font-size: 30px;
    font-weight: 730;
    line-height: 1.25;
    color: #202124;
}

.home-message {
    max-width: 760px;
    margin: 10px auto 0;
    font-size: 16px;
    line-height: 1.65;
    color: #777777;
}

.home-note {
    margin-top: 24px;
    font-size: 11px;
    color: #a2a2a2;
}


/* =========================================================
   MESSAGES
   ========================================================= */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.7;
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

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
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 7px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-note {
    text-align: center;
    color: #a4a4a4;
    font-size: 10px;
    margin-top: 12px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .home-wrap {
        padding-top: 50px;
    }

    .home-title {
        font-size: 31px;
    }

    .home-description {
        font-size: 16px;
    }

    .home-greeting {
        font-size: 25px;
    }

    .home-message {
        font-size: 14px;
    }

    .st-key-user-menu {
        width: calc(100vw - 20px) !important;
        max-width: 292px !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    if "current_chat_id" not in st.session_state:

        chats = load_chats()

        if chats:

            st.session_state.current_chat_id = (
                chats[0]["id"]
            )

        else:

            new_chat = create_chat()

            save_chat(new_chat)

            st.session_state.current_chat_id = (
                new_chat["id"]
            )

    defaults = {

        "search_text": "",

        "pending_question": None,

        "editing_index": None,

        "attachment_signature": "",

        "show_sources": True,

        "show_analytics": False,

        "share_chat_id": None,

        "greeting": random.choice(
            [
                "Hey there 👋",
                "Good to see you 👋",
                "Hey, ready when you are 👋",
                "Welcome back 👋",
                "Hey there, let’s get started 👋",
            ]
        ),
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


initialize_session_state()


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


def reset_chat_state():

    st.session_state.pending_question = None

    st.session_state.editing_index = None

    st.session_state.attachment_signature = ""

    st.session_state.share_chat_id = None


def create_new_chat():

    new_chat = create_chat()

    save_chat(new_chat)

    set_chat_metadata(
        new_chat["id"]
    )

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    reset_chat_state()

    st.session_state.show_analytics = False

    st.session_state.search_text = ""

    st.rerun()


def trim_chat(
    chat,
    message_index,
):

    if message_index < 0:
        return

    chat["messages"] = (
        chat.get(
            "messages",
            [],
        )[:message_index]
    )

    save_chat(chat)


def safe_chat_title(chat):

    title = str(
        chat.get(
            "title",
            "New Chat",
        )
    ).strip()

    return title or "New Chat"


# ============================================================
# SIDEBAR CHAT SORTING
# ============================================================

def get_sidebar_chats(
    chats,
    include_archived=False,
):

    result = []

    for chat in chats:

        metadata = get_chat_metadata(
            chat["id"]
        )

        if (
            metadata["archived"]
            and not include_archived
        ):
            continue

        item = dict(chat)

        item["_metadata"] = metadata

        result.append(item)

    pinned = []

    normal = []

    for item in result:

        if item["_metadata"]["pinned"]:

            pinned.append(item)

        else:

            normal.append(item)

    pinned.sort(
        key=lambda item: str(
            item.get(
                "updated_at",
                "",
            )
        ),
        reverse=True,
    )

    normal.sort(
        key=lambda item: str(
            item.get(
                "updated_at",
                "",
            )
        ),
        reverse=True,
    )

    return pinned + normal


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


def get_source_group(source):

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
    sources
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

    total = len(grouped)

    source_label = (
        "source"
        if total == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {total} {source_label}",
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

            else:

                st.markdown(
                    "📚 **Knowledge Base**"
                )

            section_label = (
                "section"
                if len(items) == 1
                else "sections"
            )

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
    chat
):

    lines = [
        f"# {safe_chat_title(chat)}",
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
# CHAT ACTIONS
# ============================================================

def delete_current_chat(
    chat
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

    delete_chat_metadata(
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

    reset_chat_state()

    st.rerun()


def delete_all_conversations():

    chat_ids = [
        item["id"]
        for item in load_chats()
    ]

    delete_all_chats()

    delete_all_conversation_files(
        chat_ids
    )

    delete_chat_metadata(
        chat_ids
    )

    replacement = create_chat()

    save_chat(
        replacement
    )

    st.session_state.current_chat_id = (
        replacement["id"]
    )

    reset_chat_state()

    st.rerun()


def toggle_pin(
    chat
):

    metadata = get_chat_metadata(
        chat["id"]
    )

    set_chat_metadata(
        chat["id"],
        pinned=not metadata["pinned"],
    )

    st.rerun()


def toggle_archive(
    chat
):

    metadata = get_chat_metadata(
        chat["id"]
    )

    currently_archived = (
        metadata["archived"]
    )

    set_chat_metadata(
        chat["id"],
        archived=not currently_archived,
    )

    if (
        not currently_archived
        and chat["id"]
        == st.session_state.current_chat_id
    ):

        visible = get_sidebar_chats(
            load_chats()
        )

        if visible:

            st.session_state.current_chat_id = (
                visible[0]["id"]
            )

        else:

            replacement = create_chat()

            save_chat(
                replacement
            )

            st.session_state.current_chat_id = (
                replacement["id"]
            )

    reset_chat_state()

    st.rerun()


# ============================================================
# QUESTION PROCESSING
# ============================================================

def process_question(
    question
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

        lowered = (
            error_text.lower()
        )

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

    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="sidebar-logo">✦</span>
            <span class="sidebar-name">
                AI Support
            </span>
        </div>

        <div class="sidebar-caption">
            Intelligent customer service assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # SEARCH + NEW CHAT
    # --------------------------------------------------------

    search_col, new_chat_col = st.columns(
        [
            1.1,
            6.4,
        ]
    )

    with search_col:

        if hasattr(
            st,
            "popover",
        ):

            search_menu = st.popover(
                "⌕",
                help="Search conversations",
            )

        else:

            search_menu = None

    if search_menu is not None:

        with search_menu:

            search_value = st.text_input(
                "Search",
                value=st.session_state.search_text,
                placeholder="Search chats...",
                label_visibility="collapsed",
                key="chat_search_input",
            )

            st.session_state.search_text = (
                search_value
            )

    else:

        search_value = st.text_input(
            "Search",
            value=st.session_state.search_text,
            placeholder="Search chats...",
            label_visibility="collapsed",
            key="chat_search_fallback",
        )

        st.session_state.search_text = (
            search_value
        )

    with new_chat_col:

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

    visible_chats = get_sidebar_chats(
        visible_chats,
        include_archived=False,
    )

    cleaned_chats = []

    for item in visible_chats:

        title = safe_chat_title(
            item
        )

        messages = item.get(
            "messages",
            [],
        )

        if (
            not messages
            and title.lower()
            == "new chat"
            and item["id"]
            != st.session_state.current_chat_id
        ):

            continue

        cleaned_chats.append(
            item
        )

    visible_chats = cleaned_chats[:12]

    if not visible_chats:

        st.caption(
            "No conversations yet."
        )

    # --------------------------------------------------------
    # CHAT ROWS
    # --------------------------------------------------------

    for item in visible_chats:

        item_id = str(
            item["id"]
        )

        full_title = safe_chat_title(
            item
        )

        display_title = full_title

        if len(display_title) > 31:

            display_title = (
                display_title[:28]
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

        with st.container(
            key=f"chat-row-{item_id}"
        ):

            chat_col, action_col = st.columns(
                [
                    8.6,
                    1.25,
                ]
            )

            with chat_col:

                if st.button(
                    display_title,
                    use_container_width=True,
                    key=f"chat-open-{item_id}",
                    help=full_title,
                ):

                    st.session_state.current_chat_id = (
                        item_id
                    )

                    reset_chat_state()

                    st.session_state.show_analytics = (
                        False
                    )

                    st.rerun()

            with action_col:

                if hasattr(
                    st,
                    "popover",
                ):

                    action_menu = st.popover(
                        "⋯",
                        help="Chat actions",
                    )

                else:

                    action_menu = st.expander(
                        "⋯",
                        expanded=False,
                    )

                with action_menu:

                    current_item = find_chat(
                        load_chats(),
                        item_id,
                    )

                    if current_item is None:
                        continue

                    metadata = get_chat_metadata(
                        item_id
                    )

                    st.markdown(
                        """
                        <div class="chat-menu-title">
                            Chat actions
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # ----------------------------------------
                    # SHARE
                    # ----------------------------------------

                    if st.button(
                        "↗  Share",
                        use_container_width=True,
                        key=f"share-{item_id}",
                    ):

                        st.session_state.share_chat_id = (
                            item_id
                        )

                        st.rerun()

                    # ----------------------------------------
                    # EXPORT
                    # ----------------------------------------

                    st.download_button(
                        "⇩  Export",
                        data=export_markdown(
                            current_item
                        ),
                        file_name="conversation.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key=f"export-{item_id}",
                    )

                    # ----------------------------------------
                    # RENAME
                    # ----------------------------------------

                    if st.button(
                        "✎  Rename",
                        use_container_width=True,
                        key=f"rename-open-{item_id}",
                    ):

                        st.session_state[
                            f"rename_open_{item_id}"
                        ] = True

                        st.rerun()

                    # ----------------------------------------
                    # PIN
                    # ----------------------------------------

                    pin_label = (
                        "⌖  Unpin chat"
                        if metadata["pinned"]
                        else "⌖  Pin chat"
                    )

                    if st.button(
                        pin_label,
                        use_container_width=True,
                        key=f"pin-{item_id}",
                    ):

                        toggle_pin(
                            current_item
                        )

                    # ----------------------------------------
                    # ARCHIVE
                    # ----------------------------------------

                    archive_label = (
                        "▣  Unarchive"
                        if metadata["archived"]
                        else "▣  Archive"
                    )

                    if st.button(
                        archive_label,
                        use_container_width=True,
                        key=f"archive-{item_id}",
                    ):

                        toggle_archive(
                            current_item
                        )

                    st.divider()

                    # ----------------------------------------
                    # MOVE TO PROJECT
                    # ----------------------------------------

                    st.markdown(
                        "**Move to project**"
                    )

                    project_options = [
                        "No project",
                        "Customer Support",
                        "AI Projects",
                        "Internship",
                    ]

                    current_project = (
                        metadata.get(
                            "project",
                            "",
                        )
                    )

                    current_project_label = (
                        current_project
                        or "No project"
                    )

                    if (
                        current_project_label
                        not in project_options
                    ):

                        current_project_label = (
                            "No project"
                        )

                    selected_project = st.selectbox(
                        "Project",
                        project_options,
                        index=project_options.index(
                            current_project_label
                        ),
                        key=f"project-{item_id}",
                        label_visibility="collapsed",
                    )

                    if (
                        selected_project
                        != current_project_label
                    ):

                        if (
                            selected_project
                            == "No project"
                        ):

                            selected_project = ""

                        set_chat_metadata(
                            item_id,
                            project=selected_project,
                        )

                        st.rerun()

                    st.divider()

                    # ----------------------------------------
                    # DELETE
                    # ----------------------------------------

                    if st.button(
                        "🗑  Delete",
                        use_container_width=True,
                        key=f"delete-{item_id}",
                    ):

                        delete_current_chat(
                            current_item
                        )

            # --------------------------------------------
            # RENAME PANEL
            # --------------------------------------------

            if st.session_state.get(
                f"rename_open_{item_id}",
                False,
            ):

                rename_value = st.text_input(
                    "Rename chat",
                    value=full_title,
                    key=f"rename-input-{item_id}",
                )

                save_col, cancel_col = st.columns(
                    2
                )

                with save_col:

                    if st.button(
                        "Save",
                        use_container_width=True,
                        key=f"rename-save-{item_id}",
                    ):

                        if rename_value.strip():

                            rename_chat(
                                current_item,
                                rename_value.strip(),
                            )

                            st.session_state[
                                f"rename_open_{item_id}"
                            ] = False

                            st.rerun()

                with cancel_col:

                    if st.button(
                        "Cancel",
                        use_container_width=True,
                        key=f"rename-cancel-{item_id}",
                    ):

                        st.session_state[
                            f"rename_open_{item_id}"
                        ] = False

                        st.rerun()

    # --------------------------------------------------------
    # FIXED USER MENU
    # --------------------------------------------------------

    with st.container(
        key="user-menu"
    ):

        if hasattr(
            st,
            "popover",
        ):

            user_menu = st.popover(
                "◉  Aayan Shaikh",
                help="Account and settings",
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

            st.session_state.show_sources = (
                st.checkbox(
                    "Show sources",
                    value=st.session_state.show_sources,
                    key="settings_show_sources",
                )
            )

            st.divider()

            st.markdown(
                "**Current conversation**"
            )

            settings_title = st.text_input(
                "Conversation title",
                value=safe_chat_title(chat),
                key="settings_title",
            )

            if st.button(
                "Save title",
                use_container_width=True,
                key="settings_save_title",
            ):

                if settings_title.strip():

                    rename_chat(
                        chat,
                        settings_title.strip(),
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
                key="settings_export",
            )

            if st.button(
                "Analytics",
                use_container_width=True,
                key="settings_analytics",
            ):

                st.session_state.show_analytics = (
                    True
                )

                st.rerun()

            st.divider()

            if st.button(
                "Delete current chat",
                use_container_width=True,
                key="settings_delete_current",
            ):

                delete_current_chat(
                    chat
                )

            if st.button(
                "Delete all chats",
                use_container_width=True,
                key="settings_delete_all",
            ):

                delete_all_conversations()

            st.caption(
                "AI Customer Service Assistant"
            )


# ============================================================
# SHARE PANEL
# ============================================================

if st.session_state.share_chat_id:

    shared_chat = find_chat(
        load_chats(),
        st.session_state.share_chat_id,
    )

    if shared_chat is not None:

        with st.expander(
            f"Share · {safe_chat_title(shared_chat)}",
            expanded=True,
        ):

            st.caption(
                "Copy the conversation text below to share it."
            )

            st.text_area(
                "Conversation",
                value=export_markdown(
                    shared_chat
                ),
                height=220,
                key="share_conversation_text",
            )

            if st.button(
                "Close",
                key="close_share_panel",
            ):

                st.session_state.share_chat_id = (
                    None
                )

                st.rerun()


# ============================================================
# TOP BAR
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
        <div class="main-topbar">
            <span class="main-topbar-title">
                {safe_chat_title(chat)}
            </span>

            <span class="main-topbar-subtitle">
                AI Customer Service Assistant
            </span>
        </div>
        """,
        unsafe_allow_html=True,
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

            st.session_state.show_analytics = (
                False
            )

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

            st.session_state.show_analytics = (
                False
            )

            st.rerun()

        st.stop()


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
            index % number_of_columns
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
                [
                    9,
                    1,
                ]
            )

            with left:

                st.write(
                    f"📄 {filename}"
                )

            with right:

                if st.button(
                    "×",
                    key=f"remove-file-{file_id}",
                    help="Remove attachment",
                ):

                    removed = (
                        remove_conversation_file(
                            chat["id"],
                            file_id,
                        )
                    )

                    if removed:

                        st.session_state.attachment_signature = (
                            ""
                        )

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
        <div class="home-wrap">

            <div class="home-logo">
                ✦
            </div>

            <div class="home-title">
                AI Customer Service Assistant
            </div>

            <div class="home-description">
                Ask questions and get reliable answers
                from your support knowledge base,
                or attach a document and ask about
                its contents.
            </div>

            <div class="home-greeting">
                {greeting}
            </div>

            <div class="home-message">
                I'm ready whenever you are.
                Ask me something, describe a customer
                issue, or attach a document and ask me
                about it.
            </div>

            <div class="home-note">
                AI Support may occasionally make mistakes.
                Verify important information.
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
        # USER EDIT MODE
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
                key=f"edit-text-{index}",
                height=100,
            )

            save_col, cancel_col = (
                st.columns(2)
            )

            with save_col:

                if st.button(
                    "Save & regenerate",
                    type="primary",
                    use_container_width=True,
                    key=f"save-edit-{index}",
                ):

                    clean_text = (
                        edited_text.strip()
                    )

                    if not clean_text:

                        st.warning(
                            "Message cannot be empty."
                        )

                    else:

                        trim_chat(
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

            with cancel_col:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key=f"cancel-edit-{index}",
                ):

                    st.session_state.editing_index = (
                        None
                    )

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
                    key=f"like-{index}",
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
                    key=f"dislike-{index}",
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
                    key=f"regenerate-{index}",
                    help="Regenerate",
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
                    key=f"edit-{index}",
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

    st.session_state.pending_question = (
        None
    )

    process_question(
        pending_question
    )


# ============================================================
# CHAT INPUT CAPABILITIES
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
# MODERN CHAT COMPOSER
# ============================================================

if supports_accept_file:

    chat_input_kwargs = {
        "placeholder":
            "Message AI Support...",
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
        ]

    composer = st.chat_input(
        **chat_input_kwargs
    )

    if composer is not None:

        composer_text = ""

        composer_files = []

        # ----------------------------------------------------
        # TEXT
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

        # ----------------------------------------------------
        # DOCUMENT ATTACHMENTS
        # ----------------------------------------------------

        if composer_files:

            try:

                signature = (
                    get_attachment_signature(
                        composer_files
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
                        for item in composer_files
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
                            composer_files,
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
                        "The attached document "
                        "could not be processed."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(error)
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

    fallback_files = (
        st.file_uploader(
            "Attach documents",
            type=[
                "pdf",
                "docx",
                "txt",
                "csv",
            ],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="fallback-file-uploader",
        )
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
                    "The attached document "
                    "could not be processed."
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

if has_messages:

    st.markdown(
        """
        <div class="app-note">
            AI Support may occasionally make mistakes.
            Verify important information.
        </div>
        """,
        unsafe_allow_html=True,
    )