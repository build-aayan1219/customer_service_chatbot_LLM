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
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>

:root {
    --accent: #e85d5d;
    --accent-hover: #d94e4e;
    --text: #202124;
    --muted: #777777;
    --soft: #f7f7f7;
    --border: #e5e5e5;
}

/* Main application */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 1080px;
    padding-top: 0.4rem;
    padding-bottom: 120px;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background: #fbfbfb;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebarContent"] {
    padding: 18px 14px;
}

[data-testid="stSidebar"] .stButton > button {
    min-height: 38px;
    border-radius: 9px;
    font-size: 12px;
}

[data-testid="stSidebar"] input {
    border-radius: 9px;
    font-size: 11px;
}


/* Header */

.header-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
}

.header-subtitle {
    font-size: 9px;
    color: #999999;
    margin-top: -5px;
}


/* Empty state */

.empty-state-space {
    height: 125px;
}

.empty-state-title {
    text-align: center;
    font-size: 28px;
    font-weight: 750;
    letter-spacing: -0.6px;
    color: var(--text);
}

.empty-state-description {
    max-width: 540px;
    margin: 8px auto 0;
    text-align: center;
    color: #858585;
    font-size: 12px;
    line-height: 1.55;
}


/* Suggestions */

.suggestion-label {
    color: #8c8c8c;
    font-size: 10px;
    margin-top: 28px;
    margin-bottom: 7px;
}

.suggestion-button {
    font-size: 11px;
}


/* Messages */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stChatMessageContent"] {
    font-size: 13px;
    line-height: 1.65;
}


/* Chat composer */

[data-testid="stChatInput"] {
    border-top: none !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 13px !important;
}


/* Small text */

.small-note {
    text-align: center;
    color: #aaaaaa;
    font-size: 9px;
    margin-top: 7px;
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

                st.caption(
                    f"Attached file · "
                    f"{len(items)} relevant "
                    f"{'section' if len(items) == 1 else 'sections'}"
                )

            else:

                st.markdown(
                    "📚 **Knowledge Base**"
                )

                st.caption(
                    f"{len(items)} relevant "
                    f"{'section' if len(items) == 1 else 'sections'}"
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
        "### AI Support"
    )

    st.caption(
        "Customer support assistant"
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
        placeholder="Search conversations...",
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

            st.rerun()


# ============================================================
# TOP BAR
# ============================================================

header_left, header_right = st.columns(
    [9, 1]
)


with header_left:

    st.markdown(
        f"**{chat.get('title', 'New Chat')}**"
    )

    st.caption(
        "Customer Support"
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
        "**Attached files**"
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
# EMPTY STATE
# ============================================================

if not chat.get(
    "messages"
):

    st.markdown(
        "<div class='empty-state-space'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='empty-state-title'>"
        "AI Support"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='empty-state-description'>"
        "Ask a support question, or attach a document "
        "and ask about its contents."
        "</div>",
        unsafe_allow_html=True,
    )


    st.markdown(
        "<div class='suggestion-label'>"
        "Suggestions"
        "</div>",
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
                use_container_width=True,
                key=(
                    "suggestion_"
                    + str(index)
                ),
            ):

                st.session_state.pending_question = (
                    suggestion
                )

                st.rerun()


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
# CHAT INPUT / FILE ATTACHMENTS
# ============================================================

chat_input_signature = inspect.signature(
    st.chat_input
)

chat_input_parameters = (
    chat_input_signature.parameters
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


if supports_accept_file:

    chat_input_kwargs = {
        "placeholder": "Message AI Support..."
    }

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

    if supports_max_uploads:

        chat_input_kwargs["accept_file"] = "multiple"
        chat_input_kwargs["max_uploads"] = 10

    else:

        chat_input_kwargs["accept_file"] = True


    composer = st.chat_input(
        **chat_input_kwargs
    )


    if composer is not None:

        composer_text = ""
        composer_files = []


        # Newer Streamlit versions return an object
        # containing text and files.

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
        # PROCESS ATTACHED DOCUMENTS
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
                Path(
                    filename
                ).suffix.lower()
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
        # ADD DOCUMENTS TO CONVERSATION
        # ----------------------------------------------------

        if document_files:

            signature = (
                get_attachment_signature(
                    document_files
                )
            )


            if (
                signature
                != st.session_state.get(
                    "attachment_signature",
                    "",
                )
            ):

                result = (
                    add_conversation_files(
                        chat["id"],
                        document_files,
                    )
                )


                st.session_state.attachment_signature = (
                    signature
                )


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
                "Selected images: "
                + ", ".join(
                    image_names
                )
            )


        # ----------------------------------------------------
        # PROCESS QUESTION
        # ----------------------------------------------------

        if composer_text:

            process_question(
                composer_text
            )


else:

    # --------------------------------------------------------
    # FALLBACK FOR OLDER STREAMLIT
    # --------------------------------------------------------

    fallback_files = st.file_uploader(
        "Attach files",
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


        if (
            signature
            != st.session_state.get(
                "attachment_signature",
                "",
            )
        ):

            result = (
                add_conversation_files(
                    chat["id"],
                    fallback_files,
                )
            )


            st.session_state.attachment_signature = (
                signature
            )


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


    question = st.chat_input(
        "Message AI Support..."
    )


    if question:

        process_question(
            question
        )


# ============================================================
# MODERN COMPOSER
# ============================================================

if supports_file_upload:

    composer = st.chat_input(
        "Message AI Support...",
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
                ).suffix.lower()
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


            if (
                signature
                != st.session_state.attachment_signature
            ):

                result = (
                    add_conversation_files(
                        chat["id"],
                        document_files,
                    )
                )


                st.session_state.attachment_signature = (
                    signature
                )


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
                "Image selected successfully. "
                "The current RAG pipeline indexes PDF, DOCX, "
                "TXT and CSV documents."
            )


            st.caption(
                "Selected images: "
                + ", ".join(
                    image_names
                )
            )


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        if composer_text:

            process_question(
                composer_text
            )


# ============================================================
# COMPATIBILITY COMPOSER
# ============================================================

else:

    st.caption(
        "Attach a file"
    )


    fallback_files = st.file_uploader(
        "Attach files",
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


        if (
            signature
            != st.session_state.attachment_signature
        ):

            result = (
                add_conversation_files(
                    chat["id"],
                    fallback_files,
                )
            )


            st.session_state.attachment_signature = (
                signature
            )


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