import inspect
import time
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

from src.langchain_helper import (
    create_vector_db,
    get_qa_stream,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Customer Service Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* Main application */

.block-container {
    max-width: 900px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}


/* Header */

.app-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #202124;
    margin-bottom: 4px;
}

.app-subtitle {
    text-align: center;
    color: #8b8f96;
    font-size: 15px;
    margin-bottom: 28px;
}


/* Welcome */

.welcome-box {
    text-align: center;
    padding: 22px 20px 20px 20px;
    margin-bottom: 18px;
}

.welcome-icon {
    font-size: 52px;
    margin-bottom: 4px;
}

.welcome-title {
    font-size: 25px;
    font-weight: 600;
    color: #252525;
    margin-top: 5px;
}

.welcome-text {
    color: #929292;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 8px;
}


/* Native buttons */

div.stButton > button {
    border-radius: 10px;
    min-height: 44px;
    font-size: 13px;
}


/* Chat messages */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.65;
}


/* Chat input */

[data-testid="stChatInput"] {
    border-top: none !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 14px !important;
}


/* Sources */

.source-header {
    font-weight: 600;
    font-size: 13px;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #fafafa;
}

[data-testid="stSidebarContent"] {
    padding-top: 1rem;
}

[data-testid="stSidebar"] .stButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-size: 12px;
}


/* Footer */

.footer {
    text-align: center;
    color: #777777;
    font-size: 12px;
    margin-top: 22px;
    padding-bottom: 10px;
}


/* Small status */

.status-text {
    font-size: 12px;
}


/* Mobile */

@media (max-width: 700px) {

    .app-title {
        font-size: 30px;
    }

    .app-subtitle {
        font-size: 13px;
    }

    .welcome-title {
        font-size: 22px;
    }

    .welcome-text {
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

        st.session_state.current_chat_id = new_chat["id"]


if "search_text" not in st.session_state:

    st.session_state.search_text = ""


if "editing_index" not in st.session_state:

    st.session_state.editing_index = None


if "pending_question" not in st.session_state:

    st.session_state.pending_question = None


if "attachment_signature" not in st.session_state:

    st.session_state.attachment_signature = ""


if "show_sources" not in st.session_state:

    st.session_state.show_sources = True


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

    st.session_state.current_chat_id = new_chat["id"]

    return new_chat


def start_new_chat():

    new_chat = create_chat()

    st.session_state.current_chat_id = new_chat["id"]

    st.session_state.editing_index = None
    st.session_state.pending_question = None
    st.session_state.attachment_signature = ""

    st.rerun()


def clear_current_chat():

    chat = get_current_chat()

    chat["messages"] = []
    chat["title"] = "New Chat"

    save_chat(chat)

    st.session_state.editing_index = None
    st.session_state.pending_question = None

    st.rerun()


def truncate_chat(chat, message_index):

    if message_index < 0:

        return

    chat["messages"] = chat.get(
        "messages",
        [],
    )[:message_index]

    if not chat["messages"]:

        chat["title"] = "New Chat"

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


def source_name(metadata):

    filename = (
        metadata.get("source_file")
        or metadata.get("file_name")
        or metadata.get("filename")
    )

    if filename:

        return Path(
            str(filename)
        ).name

    return "Knowledge Base"


def display_sources(sources):

    if not sources:

        return

    if not st.session_state.show_sources:

        return

    with st.expander(
        "📚 View Source Information",
        expanded=False,
    ):

        st.caption(
            "Information retrieved to ground this answer."
        )

        grouped = {}

        for source in sources:

            content, metadata = normalize_source(
                source
            )

            name = source_name(
                metadata
            )

            if name not in grouped:

                grouped[name] = []

            grouped[name].append(
                (
                    content,
                    metadata,
                )
            )

        for group_number, (
            name,
            items,
        ) in enumerate(
            grouped.items(),
            1,
        ):

            if name == "Knowledge Base":

                st.markdown(
                    "### 📚 Knowledge Base"
                )

            else:

                st.markdown(
                    f"### 📄 {name}"
                )

            for item_number, (
                content,
                metadata,
            ) in enumerate(
                items,
                1,
            ):

                section = (
                    metadata.get("section")
                    or metadata.get("heading")
                    or metadata.get("title")
                    or f"Relevant section {item_number}"
                )

                with st.expander(
                    str(section)
                ):

                    st.write(
                        content
                    )

            if group_number < len(grouped):

                st.divider()


# ============================================================
# EXPORT
# ============================================================

def export_conversation(chat):

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

            message = (
                "The AI service usage limit has been reached. "
                "Please try again later."
            )

        else:

            message = (
                "Sorry, I couldn't process your question."
            )

        st.error(
            message
        )

        if "429" not in lowered:

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

    st.header(
        "⚙️ Settings"
    )

    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
        type="primary",
        key="sidebar_new_chat",
    ):

        start_new_chat()


    # --------------------------------------------------------
    # CHAT SEARCH
    # --------------------------------------------------------

    st.subheader(
        "💬 Conversations"
    )

    search_text = st.text_input(
        "Search conversations",
        value=st.session_state.search_text,
        placeholder="Search chats...",
        label_visibility="collapsed",
        key="conversation_search",
    )

    st.session_state.search_text = (
        search_text
    )

    all_chats = load_chats()

    if search_text.strip():

        visible_chats = search_chats(
            all_chats,
            search_text,
        )

    else:

        visible_chats = all_chats


    for conversation in visible_chats:

        conversation_id = conversation[
            "id"
        ]

        conversation_title = str(
            conversation.get(
                "title",
                "New Chat",
            )
        )

        if len(
            conversation_title
        ) > 35:

            conversation_title = (
                conversation_title[:32]
                + "..."
            )

        if (
            conversation_id
            == st.session_state.current_chat_id
        ):

            button_text = (
                "● "
                + conversation_title
            )

        else:

            button_text = (
                conversation_title
            )

        if st.button(
            button_text,
            use_container_width=True,
            key=(
                "conversation_"
                + conversation_id
            ),
        ):

            st.session_state.current_chat_id = (
                conversation_id
            )

            st.session_state.editing_index = None
            st.session_state.pending_question = None
            st.session_state.attachment_signature = ""

            st.rerun()


    st.divider()


    # --------------------------------------------------------
    # KNOWLEDGE BASE
    # --------------------------------------------------------

    st.subheader(
        "📚 Knowledge Base"
    )

    st.caption(
        "FAQ and support information used by the chatbot."
    )

    if st.button(
        "🔄 Create / Update Knowledge Base",
        use_container_width=True,
        key="update_knowledge_base",
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


    st.success(
        "🟢 Knowledge Base Ready"
    )


    st.divider()


    # --------------------------------------------------------
    # CHAT ACTIONS
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
        key="clear_chat",
    ):

        clear_current_chat()


    st.divider()


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.subheader(
        "ℹ️ About"
    )

    st.write(
        "An AI-powered customer service assistant that "
        "uses Retrieval-Augmented Generation (RAG) to "
        "answer questions using trusted information."
    )


    st.divider()


    # --------------------------------------------------------
    # SETTINGS
    # --------------------------------------------------------

    st.subheader(
        "🔧 Chat Settings"
    )

    st.session_state.show_sources = st.checkbox(
        "Show source information",
        value=st.session_state.show_sources,
        key="show_source_toggle",
    )


    # --------------------------------------------------------
    # RENAME
    # --------------------------------------------------------

    new_title = st.text_input(
        "Conversation title",
        value=chat.get(
            "title",
            "New Chat",
        ),
        key="rename_title",
    )

    if st.button(
        "Rename Conversation",
        use_container_width=True,
        key="rename_conversation",
    ):

        if new_title.strip():

            rename_chat(
                chat,
                new_title.strip(),
            )

            st.rerun()


    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    st.download_button(
        "⬇️ Export Conversation",
        data=export_conversation(
            chat
        ),
        file_name="conversation.md",
        mime="text/markdown",
        use_container_width=True,
        key="export_conversation",
    )


    # --------------------------------------------------------
    # DELETE CURRENT CHAT
    # --------------------------------------------------------

    if st.button(
        "❌ Delete Current Chat",
        use_container_width=True,
        key="delete_current_chat",
    ):

        current_id = chat["id"]

        remaining = delete_chat(
            load_chats(),
            current_id,
        )

        delete_all_conversation_files(
            [current_id]
        )

        if remaining:

            st.session_state.current_chat_id = (
                remaining[0]["id"]
            )

        else:

            replacement = create_chat()

            st.session_state.current_chat_id = (
                replacement["id"]
            )

        st.session_state.editing_index = None
        st.session_state.pending_question = None
        st.session_state.attachment_signature = ""

        st.rerun()


    # --------------------------------------------------------
    # DELETE EVERYTHING
    # --------------------------------------------------------

    if st.button(
        "⚠️ Delete All Conversations",
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

        st.session_state.current_chat_id = (
            replacement["id"]
        )

        st.session_state.editing_index = None
        st.session_state.pending_question = None
        st.session_state.attachment_signature = ""

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # TECHNOLOGY STACK
    # --------------------------------------------------------

    st.caption(
        "Technology Stack"
    )

    st.write(
        "🤖 Gemini\n\n"
        "🔎 FAISS\n\n"
        "🧠 Hugging Face Embeddings\n\n"
        "🔗 LangChain\n\n"
        "🌐 Streamlit"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">'
    '🤖 AI Customer Service Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Ask questions and get reliable answers from our knowledge base.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# ATTACHED CONVERSATION FILES
# ============================================================

attached_files = list_conversation_files(
    chat["id"]
)


if attached_files:

    st.caption(
        "📎 Files attached to this conversation"
    )

    file_columns = st.columns(
        min(
            3,
            len(attached_files),
        )
    )

    for index, file_record in enumerate(
        attached_files
    ):

        filename = (
            file_record.get(
                "original_name"
            )
            or file_record.get(
                "file_name"
            )
            or "Attached file"
        )

        size = file_record.get(
            "size_display",
            "",
        )

        with file_columns[
            index % len(file_columns)
        ]:

            st.info(
                f"📄 {filename}\n\n"
                f"{size}"
            )

    with st.expander(
        "Manage attached files"
    ):

        for file_record in attached_files:

            file_id = file_record.get(
                "id"
            )

            filename = (
                file_record.get(
                    "original_name"
                )
                or file_record.get(
                    "file_name"
                )
                or "Attached file"
            )

            left, right = st.columns(
                [8, 1]
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
                ):

                    remove_conversation_file(
                        chat["id"],
                        file_id,
                    )

                    st.session_state.attachment_signature = ""

                    st.rerun()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not chat.get(
    "messages"
):

    st.markdown(
        """
        <div class="welcome-box">

            <div class="welcome-icon">
                💬
            </div>

            <div class="welcome-title">
                Welcome! How can I help you today?
            </div>

            <div class="welcome-text">
                I can answer questions using the available
                customer-support knowledge base, help you
                understand common issues, and answer questions
                about documents you attach to this conversation.
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
        # EDIT MODE
        # ----------------------------------------------------

        if (
            role == "user"
            and st.session_state.editing_index
            == index
        ):

            edited_message = st.text_area(
                "Edit your message",
                value=content,
                key=(
                    "edit_message_"
                    + str(index)
                ),
                height=100,
            )

            save_column, cancel_column = (
                st.columns(2)
            )

            with save_column:

                if st.button(
                    "Save & Regenerate",
                    type="primary",
                    use_container_width=True,
                    key=(
                        "save_edit_"
                        + str(index)
                    ),
                ):

                    edited_message = (
                        edited_message.strip()
                    )

                    if not edited_message:

                        st.warning(
                            "Message cannot be empty."
                        )

                    else:

                        truncate_chat(
                            chat,
                            index,
                        )

                        st.session_state.editing_index = None
                        st.session_state.pending_question = (
                            edited_message
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

        st.write(
            content
        )


        # ----------------------------------------------------
        # ASSISTANT CONTROLS
        # ----------------------------------------------------

        if role == "assistant":

            display_sources(
                message.get(
                    "sources",
                    [],
                )
            )

            action_1, action_2, action_3, action_4, action_5 = (
                st.columns(
                    [
                        0.7,
                        0.7,
                        0.7,
                        0.7,
                        6,
                    ]
                )
            )

            with action_1:

                if st.button(
                    "👍",
                    key=(
                        "positive_"
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


            with action_2:

                if st.button(
                    "👎",
                    key=(
                        "negative_"
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


            with action_3:

                if st.button(
                    "↻",
                    key=(
                        "regenerate_"
                        + str(index)
                    ),
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


            with action_4:

                if st.button(
                    "✏️",
                    key=(
                        "edit_assistant_"
                        + str(index)
                    ),
                    help="Edit previous question",
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


            with action_5:

                response_time = (
                    message.get(
                        "response_time"
                    )
                )

                if response_time is not None:

                    try:

                        st.caption(
                            f"Response time: "
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
# MODERN CHAT COMPOSER WITH ATTACHMENTS
# ============================================================

if supports_accept_file:

    chat_input_options = {
        "placeholder": "Ask your question..."
    }

    if supports_max_uploads:

        chat_input_options[
            "accept_file"
        ] = "multiple"

        chat_input_options[
            "max_uploads"
        ] = 10

    else:

        chat_input_options[
            "accept_file"
        ] = True

    if supports_file_type:

        chat_input_options[
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

    submitted = st.chat_input(
        **chat_input_options
    )

    if submitted is not None:

        question_text = ""

        uploaded_files = []

        if isinstance(
            submitted,
            str,
        ):

            question_text = (
                submitted.strip()
            )

        else:

            question_text = str(
                getattr(
                    submitted,
                    "text",
                    "",
                )
                or ""
            ).strip()

            uploaded_files = list(
                getattr(
                    submitted,
                    "files",
                    [],
                )
                or []
            )


        # ----------------------------------------------------
        # DOCUMENT ATTACHMENTS
        # ----------------------------------------------------

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
        # SAVE DOCUMENTS TO CONVERSATION
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
                                file,
                                "name",
                                "",
                            )
                        )
                        for file in document_files
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
                        "The attached document could not be processed."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(error)
                        )


        # ----------------------------------------------------
        # IMAGE NOTICE
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
                "Image understanding is not connected "
                "to the current document RAG pipeline."
            )


        # ----------------------------------------------------
        # PROCESS QUESTION
        # ----------------------------------------------------

        if question_text:

            process_question(
                question_text
            )


# ============================================================
# COMPATIBILITY COMPOSER
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
                            file,
                            "name",
                            "",
                        )
                    )
                    for file in fallback_files
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
                    "The attached document could not be processed."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(
                        str(error)
                    )


    question = st.chat_input(
        "Ask your question..."
    )

    if question:

        process_question(
            question
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'Powered by Gemini • FAISS • Hugging Face • LangChain • Streamlit'
    '</div>',
    unsafe_allow_html=True,
)