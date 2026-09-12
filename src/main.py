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
# UI STATE FILE
# Used for sidebar-only metadata such as pinned/archived chats.
# This does not depend on chat_manager having extra functions.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UI_STATE_FILE = PROJECT_ROOT / "knowledge_base" / "chat_ui_state.json"


def load_ui_state():
    import json

    try:
        if UI_STATE_FILE.exists():
            with open(
                UI_STATE_FILE,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data
    except Exception:
        pass

    return {
        "pinned": [],
        "archived": [],
    }


def save_ui_state(state):
    import json

    try:
        UI_STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            UI_STATE_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                state,
                file,
                indent=2,
            )
    except Exception:
        pass


if "ui_state" not in st.session_state:
    st.session_state.ui_state = load_ui_state()


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.2rem;
    padding-bottom: 110px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid #e6e6e6;
}

[data-testid="stSidebarContent"] {
    padding: 15px 10px 10px 10px;
}

[data-testid="stSidebar"] .stButton > button {
    border-radius: 9px;
    min-height: 38px;
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
    padding: 6px 5px 0 5px;
}

.sidebar-brand-logo {
    font-size: 23px;
    line-height: 1;
    color: #111111;
}

.sidebar-brand-name {
    font-size: 18px;
    font-weight: 750;
    color: #111111;
}

.sidebar-caption {
    margin: 7px 0 17px 31px;
    color: #8b8b8b;
    font-size: 11px;
}

.sidebar-search-button button {
    min-height: 35px !important;
    height: 35px !important;
    padding: 0 !important;
    font-size: 17px !important;
}

.sidebar-search-box {
    margin-top: 3px;
    margin-bottom: 8px;
}

.sidebar-section {
    margin: 22px 4px 8px 4px;
    color: #777777;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.recent-empty {
    color: #999999;
    font-size: 12px;
    padding: 10px 4px;
}


/* =========================================================
   CHAT ROWS
   ========================================================= */

.chat-row {
    margin-bottom: 4px;
}

.chat-row-active button {
    background: #e7e7e7 !important;
    border-color: #c9c9c9 !important;
}

.chat-action button {
    min-height: 38px !important;
    height: 38px !important;
    padding: 0 !important;
    font-size: 16px !important;
}

.chat-title-button button {
    text-align: left !important;
    padding-left: 12px !important;
    padding-right: 8px !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}


/* =========================================================
   CHAT ACTION MENU
   ========================================================= */

.chat-menu-title {
    font-size: 15px;
    font-weight: 650;
    margin-bottom: 10px;
    word-break: break-word;
}

.chat-menu-description {
    font-size: 11px;
    color: #8b8b8b;
    margin-bottom: 10px;
}


/* =========================================================
   MAIN TOP BAR
   ========================================================= */

.main-topbar {
    display: flex;
    align-items: center;
    min-height: 38px;
    border-bottom: 1px solid #eeeeee;
    margin-bottom: 2px;
}

.main-topbar-title {
    font-size: 14px;
    font-weight: 650;
    color: #242424;
}

.main-topbar-subtitle {
    margin-left: 9px;
    color: #999999;
    font-size: 11px;
}


/* =========================================================
   HOME
   ========================================================= */

.home-wrapper {
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
    padding-top: 58px;
    padding-bottom: 30px;
}

.home-logo {
    width: 76px;
    height: 76px;
    margin: 0 auto 23px auto;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f3f3f3;
    border: 1px solid #e5e5e5;
    font-size: 40px;
    color: #202124;
}

.home-title {
    font-size: 40px;
    font-weight: 760;
    letter-spacing: -1.4px;
    line-height: 1.15;
    color: #202124;
    margin-bottom: 13px;
}

.home-subtitle {
    max-width: 760px;
    margin: 0 auto;
    color: #555555;
    font-size: 18px;
    line-height: 1.55;
}

.home-greeting {
    margin-top: 38px;
    color: #202124;
    font-size: 29px;
    font-weight: 720;
    letter-spacing: -0.5px;
}

.home-message {
    max-width: 720px;
    margin: 10px auto 0 auto;
    color: #777777;
    font-size: 15px;
    line-height: 1.65;
}


/* =========================================================
   CHAT MESSAGES
   ========================================================= */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.7;
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
    margin-bottom: 6px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-footer {
    text-align: center;
    color: #aaaaaa;
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
        width: 62px;
        height: 62px;
        font-size: 32px;
    }

    .home-title {
        font-size: 30px;
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
            "Good to see you 👋",
            "Hey! Ready when you are 👋",
            "Hello there 👋",
            "Hey! What can I help you figure out today?",
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


def reset_chat_state():

    st.session_state.pending_question = None
    st.session_state.editing_index = None
    st.session_state.attachment_signature = ""
    st.session_state.show_analytics = False


def create_new_chat():

    new_chat = create_chat()

    save_chat(new_chat)

    st.session_state.current_chat_id = new_chat["id"]

    reset_chat_state()

    st.session_state.search_open = False
    st.session_state.search_text = ""

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

        return clean_question[:39] + "..."

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
# PIN / ARCHIVE HELPERS
# ============================================================

def chat_id_string(chat):

    return str(
        chat.get(
            "id",
            "",
        )
    )


def is_pinned(chat):

    return chat_id_string(chat) in [
        str(item)
        for item in st.session_state.ui_state.get(
            "pinned",
            [],
        )
    ]


def is_archived(chat):

    return chat_id_string(chat) in [
        str(item)
        for item in st.session_state.ui_state.get(
            "archived",
            [],
        )
    ]


def set_pinned(chat, value):

    chat_id = chat_id_string(chat)

    pinned = [
        str(item)
        for item in st.session_state.ui_state.get(
            "pinned",
            [],
        )
    ]

    if value:

        if chat_id not in pinned:
            pinned.append(chat_id)

    else:

        pinned = [
            item
            for item in pinned
            if item != chat_id
        ]

    st.session_state.ui_state["pinned"] = pinned

    save_ui_state(
        st.session_state.ui_state
    )


def set_archived(chat, value):

    chat_id = chat_id_string(chat)

    archived = [
        str(item)
        for item in st.session_state.ui_state.get(
            "archived",
            [],
        )
    ]

    if value:

        if chat_id not in archived:
            archived.append(chat_id)

    else:

        archived = [
            item
            for item in archived
            if item != chat_id
        ]

    st.session_state.ui_state["archived"] = archived

    save_ui_state(
        st.session_state.ui_state
    )


def remove_chat_from_ui_state(chat_id):

    chat_id = str(chat_id)

    for key in [
        "pinned",
        "archived",
    ]:

        current = [
            str(item)
            for item in st.session_state.ui_state.get(
                key,
                [],
            )
        ]

        st.session_state.ui_state[key] = [
            item
            for item in current
            if item != chat_id
        ]

    save_ui_state(
        st.session_state.ui_state
    )


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

    total_groups = len(
        grouped_sources
    )

    source_label = (
        "source"
        if total_groups == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {total_groups} {source_label}",
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

            section_label = (
                "section"
                if count == 1
                else "sections"
            )

            st.caption(
                f"{count} relevant {section_label}"
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
# DELETE CHAT
# ============================================================

def delete_current_chat(chat):

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

    remove_chat_from_ui_state(
        deleted_id
    )

    if remaining:

        st.session_state.current_chat_id = remaining[0]["id"]

    else:

        replacement = create_chat()

        save_chat(
            replacement
        )

        st.session_state.current_chat_id = replacement["id"]

    reset_chat_state()

    st.rerun()


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
    # BRAND + SINGLE SEARCH ICON
    # --------------------------------------------------------

    brand_column, search_column = st.columns(
        [
            8.5,
            1.2,
        ]
    )

    with brand_column:

        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-brand-logo">✦</span>
                <span class="sidebar-brand-name">AI Support</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with search_column:

        st.markdown(
            '<div class="sidebar-search-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "⌕",
            key="open_sidebar_search",
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
    # SEARCH INPUT ONLY WHEN SEARCH ICON IS CLICKED
    # --------------------------------------------------------

    if st.session_state.search_open:

        search_value = st.text_input(
            "Search conversations",
            value=st.session_state.search_text,
            placeholder="Search chats...",
            label_visibility="collapsed",
            key="sidebar_search_input",
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


    # Remove chats that have been deleted from UI metadata.
    valid_ids = {
        chat_id_string(item)
        for item in all_chats
    }

    for state_key in [
        "pinned",
        "archived",
    ]:

        st.session_state.ui_state[state_key] = [
            str(item)
            for item in st.session_state.ui_state.get(
                state_key,
                [],
            )
            if str(item) in valid_ids
        ]


    save_ui_state(
        st.session_state.ui_state
    )


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if st.session_state.search_text.strip():

        visible_chats = search_chats(
            all_chats,
            st.session_state.search_text.strip(),
        )

    else:

        visible_chats = all_chats


    # --------------------------------------------------------
    # REMOVE EMPTY DEFAULT CHATS
    # --------------------------------------------------------

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
            and str(item["id"])
            != str(
                st.session_state.current_chat_id
            )
        ):

            continue

        cleaned_chats.append(
            item
        )


    visible_chats = cleaned_chats


    # --------------------------------------------------------
    # PINNED FIRST
    # --------------------------------------------------------

    visible_chats.sort(
        key=lambda item: (
            not is_pinned(item),
            item.get(
                "updated_at",
                "",
            ),
        )
    )


    # --------------------------------------------------------
    # LIMIT SIDEBAR HEIGHT
    # --------------------------------------------------------

    visible_chats = visible_chats[:12]


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
    # CHAT ROW
    # --------------------------------------------------------

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
            title = title[:31] + "..."


        if is_pinned(item):
            display_title = "📌 " + title
        else:
            display_title = title


        is_current = (
            item_id
            == str(
                st.session_state.current_chat_id
            )
        )


        chat_column, menu_column = st.columns(
            [
                8.2,
                1.2,
            ],
            gap="small",
        )


        with chat_column:

            if is_current:

                button_label = "● " + display_title

            else:

                button_label = display_title


            if st.button(
                button_label,
                use_container_width=True,
                key="chat_select_" + item_id,
            ):

                st.session_state.current_chat_id = item_id

                reset_chat_state()

                st.rerun()


        with menu_column:

            # ------------------------------------------------
            # INLINE THREE-DOT MENU
            # ------------------------------------------------

            if hasattr(
                st,
                "popover",
            ):

                menu = st.popover(
                    "⋯",
                    key="chat_menu_" + item_id,
                )

                with menu:

                    st.markdown(
                        '<div class="chat-menu-title">'
                        + title
                        + "</div>",
                        unsafe_allow_html=True,
                    )


                    # SHARE

                    st.download_button(
                        "↗  Share",
                        data=export_markdown(
                            item
                        ),
                        file_name=(
                            "conversation_"
                            + item_id[:8]
                            + ".md"
                        ),
                        mime="text/markdown",
                        use_container_width=True,
                        key="share_chat_" + item_id,
                    )


                    # RENAME

                    rename_key = (
                        "rename_input_"
                        + item_id
                    )

                    rename_value = st.text_input(
                        "Rename",
                        value=str(
                            item.get(
                                "title",
                                "New Chat",
                            )
                        ),
                        key=rename_key,
                        label_visibility="collapsed",
                    )


                    if st.button(
                        "✎  Rename",
                        use_container_width=True,
                        key="rename_chat_" + item_id,
                    ):

                        clean_title = (
                            rename_value.strip()
                        )

                        if clean_title:

                            rename_chat(
                                item,
                                clean_title,
                            )

                            st.rerun()


                    st.divider()


                    # PIN

                    if is_pinned(item):

                        pin_label = "📌  Unpin chat"

                    else:

                        pin_label = "📌  Pin chat"


                    if st.button(
                        pin_label,
                        use_container_width=True,
                        key="pin_chat_" + item_id,
                    ):

                        set_pinned(
                            item,
                            not is_pinned(item),
                        )

                        st.rerun()


                    # ARCHIVE

                    if is_archived(item):

                        archive_label = (
                            "▣  Unarchive"
                        )

                    else:

                        archive_label = (
                            "▣  Archive"
                        )


                    if st.button(
                        archive_label,
                        use_container_width=True,
                        key="archive_chat_" + item_id,
                    ):

                        set_archived(
                            item,
                            not is_archived(item),
                        )

                        st.rerun()


                    # DELETE

                    st.divider()


                    if st.button(
                        "🗑  Delete",
                        use_container_width=True,
                        key="delete_chat_" + item_id,
                    ):

                        delete_current_chat(
                            item
                        )


                    # PROJECT

                    st.divider()

                    st.caption(
                        "Projects"
                    )

                    st.button(
                        "＋  Move to project",
                        use_container_width=True,
                        key="project_chat_" + item_id,
                        disabled=True,
                    )

                    st.caption(
                        "Project organization can be connected later."
                    )


            else:

                # ------------------------------------------------
                # FALLBACK FOR OLDER STREAMLIT
                # ------------------------------------------------

                if st.button(
                    "⋯",
                    use_container_width=True,
                    key="chat_menu_fallback_" + item_id,
                ):

                    st.session_state[
                        "selected_chat_menu"
                    ] = item_id

                    st.rerun()


    # --------------------------------------------------------
    # USER MENU
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="height: 65px;"></div>
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
            key="settings_conversation_title",
        )


        if st.button(
            "Rename conversation",
            use_container_width=True,
            key="settings_rename",
        ):

            clean_title = (
                edited_title.strip()
            )

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

            save_chat(
                chat
            )

            reset_chat_state()

            st.rerun()


        if st.button(
            "Delete conversation",
            use_container_width=True,
            key="settings_delete",
        ):

            delete_current_chat(
                chat
            )


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

            delete_all_conversation_files(
                chat_ids
            )

            st.session_state.ui_state = {
                "pinned": [],
                "archived": [],
            }

            save_ui_state(
                st.session_state.ui_state
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

if has_messages:

    chat_title = str(
        chat.get(
            "title",
            "Conversation",
        )
    )

    st.markdown(
        f"""
        <div class="main-topbar">
            <span class="main-topbar-title">
                {chat_title}
            </span>
            <span class="main-topbar-subtitle">
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


            left_column, right_column = st.columns(
                [
                    9,
                    1,
                ]
            )


            with left_column:

                st.write(
                    "📄 " + filename
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
#
# IMPORTANT:
# This uses native Streamlit markdown only for text.
# There is deliberately NO nested HTML string here.
# ============================================================

if not has_messages:

    st.markdown(
        '<div class="home-wrapper">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="home-logo">✦</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 🤖 AI Customer Service Assistant",
    )

    st.markdown(
        '<div class="home-subtitle">'
        "Ask questions and get reliable answers "
        "from your knowledge base."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="home-greeting">'
        + st.session_state.greeting
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="home-message">'
        "I'm ready whenever you are. Ask me something, "
        "describe a customer issue, or attach a document "
        "and ask me about it."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "</div>",
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


            with action_columns[0]:

                if st.button(
                    "👍",
                    key="message_like_" + str(index),
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
                    key="message_dislike_" + str(index),
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
                    key="message_regenerate_" + str(index),
                    help="Regenerate response",
                ):

                    if index > 0:

                        previous_message = (
                            chat["messages"][
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
                    key="message_edit_" + str(index),
                    help="Edit question",
                ):

                    if index > 0:

                        previous_message = (
                            chat["messages"][
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
        # DOCUMENT ATTACHMENTS
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
                + ", ".join(
                    image_names
                )
            )


            st.caption(
                "Document Q&A currently supports PDF, DOCX, TXT and CSV files."
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