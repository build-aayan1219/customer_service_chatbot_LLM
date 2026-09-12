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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Support",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
<style>

:root {
    --accent: #ff6b6b;
    --accent-dark: #e95757;
    --text: #171717;
    --secondary: #666666;
    --muted: #8d8d8d;
    --border: #e7e7e7;
    --surface: #fafafa;
    --surface-dark: #f4f4f4;
}


/* ----------------------------------------------------------
   APPLICATION
---------------------------------------------------------- */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1120px;
    padding-top: 0.8rem;
    padding-bottom: 120px;
}


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid #e5e5e5;
}

[data-testid="stSidebarContent"] {
    padding: 26px 18px 20px 18px;
}

[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px;
    min-height: 40px;
    font-size: 12px;
    font-weight: 500;
}

[data-testid="stSidebar"] input {
    border-radius: 10px;
    font-size: 12px;
}


/* ----------------------------------------------------------
   BRAND
---------------------------------------------------------- */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}

.sidebar-logo {
    font-size: 21px;
    line-height: 1;
    font-weight: 700;
    color: #111111;
}

.sidebar-brand-name {
    font-size: 17px;
    line-height: 1;
    font-weight: 750;
    color: #111111;
}

.sidebar-subtitle {
    margin-top: 7px;
    margin-bottom: 20px;
    color: #888888;
    font-size: 11px;
}


/* ----------------------------------------------------------
   TOP BAR
---------------------------------------------------------- */

.top-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-top: 2px;
}

.top-subtitle {
    font-size: 10px;
    color: #929292;
    margin-top: -4px;
}


/* ----------------------------------------------------------
   WELCOME AREA
---------------------------------------------------------- */

.welcome-container {
    max-width: 760px;
    margin: 105px auto 0 auto;
    text-align: center;
}

.welcome-logo {
    width: 58px;
    height: 58px;
    margin: 0 auto 20px auto;
    border-radius: 18px;
    background: #fff3f3;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    font-size: 31px;
    font-weight: 700;
}

.welcome-greeting {
    font-size: 31px;
    line-height: 1.2;
    letter-spacing: -0.9px;
    font-weight: 750;
    color: #161616;
    margin-bottom: 13px;
}

.welcome-title {
    font-size: 17px;
    line-height: 1.5;
    font-weight: 500;
    color: #4f4f4f;
    margin-bottom: 9px;
}

.welcome-description {
    max-width: 650px;
    margin: 0 auto;
    color: #858585;
    font-size: 13px;
    line-height: 1.7;
}


/* ----------------------------------------------------------
   CAPABILITY CARDS
---------------------------------------------------------- */

.capabilities {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 30px;
}

.capability {
    border: 1px solid #e9e9e9;
    border-radius: 11px;
    padding: 11px 17px;
    background: #ffffff;
    color: #666666;
    font-size: 11px;
}

.capability strong {
    color: #333333;
    font-weight: 650;
}


/* ----------------------------------------------------------
   WELCOME FOOTNOTE
---------------------------------------------------------- */

.welcome-footnote {
    margin-top: 27px;
    color: #a0a0a0;
    font-size: 10px;
}


/* ----------------------------------------------------------
   CHAT
---------------------------------------------------------- */

[data-testid="stChatMessage"] {
    padding-top: 10px;
    padding-bottom: 10px;
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


/* ----------------------------------------------------------
   ATTACHMENTS
---------------------------------------------------------- */

.attachment-title {
    font-size: 12px;
    font-weight: 650;
    color: #444444;
    margin-bottom: 7px;
}


/* ----------------------------------------------------------
   SMALL TEXT
---------------------------------------------------------- */

.small-note {
    text-align: center;
    color: #aaaaaa;
    font-size: 10px;
    margin-top: 10px;
}


/* ----------------------------------------------------------
   RESPONSIVE
---------------------------------------------------------- */

@media (max-width: 800px) {

    .welcome-container {
        margin-top: 65px;
    }

    .welcome-greeting {
        font-size: 25px;
    }

    .welcome-title {
        font-size: 15px;
    }

    .welcome-description {
        font-size: 12px;
        padding: 0 15px;
    }

    .capabilities {
        flex-direction: column;
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
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


if "welcome_greeting" not in st.session_state:

    greetings = [
        "Good to see you — what can I help you with?",
        "Welcome back — let's get something solved.",
        "Hey there — your support assistant is ready.",
        "Ready when you are — ask me anything.",
        "Hello — let's find the answer together.",
        "What would you like to figure out today?",
        "Welcome — your AI support workspace is ready.",
        "Let's get started — what do you need help with?",
    ]

    st.session_state.welcome_greeting = random.choice(
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

    greetings = [
        "Good to see you — what can I help you with?",
        "Welcome back — let's get something solved.",
        "Hey there — your support assistant is ready.",
        "Ready when you are — ask me anything.",
        "Hello — let's find the answer together.",
        "What would you like to figure out today?",
        "Welcome — your AI support workspace is ready.",
        "Let's get started — what do you need help with?",
    ]

    st.session_state.welcome_greeting = random.choice(
        greetings
    )

    st.rerun()


def trim_chat(chat, message_index):

    if message_index < 0:
        return

    chat["messages"] = chat.get(
        "messages",
        [],
    )[:message_index]

    save_chat(chat)


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


def get_source_group(source):

    content, metadata = normalize_source(
        source
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

    grouped = defaultdict(list)

    for source in sources:

        kind, name, content, metadata = (
            get_source_group(source)
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

    source_count = len(grouped)

    source_word = (
        "source"
        if source_count == 1
        else "sources"
    )

    with st.expander(
        f"Sources · {source_count} {source_word}",
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

                section_word = (
                    "section"
                    if len(items) == 1
                    else "sections"
                )

                st.caption(
                    f"Attached file · "
                    f"{len(items)} relevant "
                    f"{section_word}"
                )

            else:

                st.markdown(
                    "📚 **Knowledge Base**"
                )

                section_word = (
                    "section"
                    if len(items) == 1
                    else "sections"
                )

                st.caption(
                    f"{len(items)} relevant "
                    f"{section_word}"
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

chat = get_current_chat()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="sidebar-logo">✦</span>
            <span class="sidebar-brand-name">AI Support</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Intelligent customer service assistant'
        '</div>',
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
        "**Search**"
    )

    search_text = st.text_input(
        "Search conversations",
        value=st.session_state.search_text,
        placeholder="Search chats...",
        label_visibility="collapsed",
        key="sidebar_search",
    )

    st.session_state.search_text = (
        search_text
    )

    chats = load_chats()

    if search_text.strip():

        visible_chats = search_chats(
            chats,
            search_text,
        )

    else:

        visible_chats = chats

    st.markdown(
        "**Recent chats**"
    )

    if not visible_chats:

        st.caption(
            "No conversations found."
        )

    for item in visible_chats:

        item_id = item["id"]

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        )

        if len(title) > 36:

            title = (
                title[:33]
                + "..."
            )

        if (
            item_id
            == st.session_state.current_chat_id
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
            key="history_" + item_id,
        ):

            st.session_state.current_chat_id = (
                item_id
            )

            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()


# ============================================================
# TOP BAR
# ============================================================

header_left, header_right = st.columns(
    [9, 1]
)


with header_left:

    st.markdown(
        f'<div class="top-title">'
        f'{chat.get("title", "New Chat")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="top-subtitle">'
        'Customer Support'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    if hasattr(
        st,
        "popover",
    ):

        settings = st.popover(
            "⚙",
            use_container_width=True,
        )

    else:

        settings = st.expander(
            "⚙",
            expanded=False,
        )

    with settings:

        st.markdown(
            "### Settings"
        )

        st.session_state.show_sources = (
            st.checkbox(
                "Show sources",
                value=st.session_state.show_sources,
                key="settings_sources",
            )
        )

        st.divider()

        st.markdown(
            "**Conversation**"
        )

        new_title = st.text_input(
            "Conversation title",
            value=chat.get(
                "title",
                "New Chat",
            ),
            key="settings_title",
        )

        if st.button(
            "Rename",
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
            "Export conversation",
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
            "Delete conversation",
            use_container_width=True,
            key="settings_delete",
        ):

            deleted_id = chat["id"]

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

            st.session_state.pending_question = None
            st.session_state.editing_index = None
            st.session_state.attachment_signature = ""

            st.rerun()

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
            key="back_to_chat",
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
            "← Back to conversation",
            key="analytics_error_back",
        ):

            st.session_state.show_analytics = False

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
        '<div class="attachment-title">'
        'Attached files'
        '</div>',
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

        size_display = (
            record.get(
                "size_display",
                "",
            )
        )

        chunk_count = (
            record.get(
                "chunk_count",
                0,
            )
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
                    f"📄 {filename}"
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
# WELCOME / EMPTY CHAT
# ============================================================

if not chat.get(
    "messages"
):

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-logo">
                ✦
            </div>

        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="welcome-greeting">
            {st.session_state.welcome_greeting}
        </div>

        <div class="welcome-title">
            AI Support is your intelligent customer service workspace.
        </div>

        <div class="welcome-description">
            Ask questions about your support knowledge base,
            get help with common customer issues, or attach a
            document and ask questions about its contents.
        </div>

        <div class="capabilities">

            <div class="capability">
                ✦ <strong>Knowledge Base</strong>
                &nbsp;·&nbsp; Support answers
            </div>

            <div class="capability">
                📄 <strong>Document Q&A</strong>
                &nbsp;·&nbsp; Ask about files
            </div>

            <div class="capability">
                ◌ <strong>Conversation Context</strong>
                &nbsp;·&nbsp; Follow-up questions
            </div>

        </div>

        <div class="welcome-footnote">
            Attach a document from the composer below whenever
            you want answers grounded in its contents.
        </div>

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
                key=(
                    "edit_text_"
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
                    key=(
                        "cancel_edit_"
                        + str(index)
                    ),
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
# STREAMLIT CHAT INPUT CAPABILITY DETECTION
# ============================================================

chat_input_parameters = inspect.signature(
    st.chat_input
).parameters

supports_accept_file = (
    "accept_file" in chat_input_parameters
)

supports_file_type = (
    "file_type" in chat_input_parameters
)

supports_max_uploads = (
    "max_uploads" in chat_input_parameters
)


# ============================================================
# MODERN COMPOSER
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

        # ----------------------------------------------------
        # EXTRACT TEXT AND FILES
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # CLASSIFY FILES
        # ----------------------------------------------------

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
                                uploaded_file,
                                "name",
                                "",
                            )
                        )
                        for uploaded_file
                        in document_files
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

        # ----------------------------------------------------
        # IMAGE PROCESSING
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
                "Image understanding is not yet connected "
                "to the current document RAG pipeline."
            )

        # ----------------------------------------------------
        # QUESTION PROCESSING
        # ----------------------------------------------------

        if composer_text:

            process_question(
                composer_text
            )


# ============================================================
# COMPATIBILITY FALLBACK
# ============================================================

else:

    st.markdown(
        "Attach a file"
    )

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
                            uploaded_file,
                            "name",
                            "",
                        )
                    )
                    for uploaded_file
                    in fallback_files
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
    "<div class='small-note'>"
    "AI Support may occasionally make mistakes. "
    "Verify important information."
    "</div>",
    unsafe_allow_html=True,
)