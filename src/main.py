import sys
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ==================================================
# PATH
# ==================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if str(BASE_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BASE_DIR),
    )


# ==================================================
# CHAT MANAGER
# ==================================================

from src.chat_manager import (
    add_message,
    create_chat,
    delete_all_chats,
    delete_chat,
    find_chat,
    load_chats,
    rename_chat,
    search_chats,
    update_message_feedback,
)


# ==================================================
# RAG
# ==================================================

from src.langchain_helper import (
    get_qa_stream,
)


# ==================================================
# CONVERSATION FILES
# ==================================================

from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    delete_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
<style>

.title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #777;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.welcome-box {
    max-width: 700px;
    margin: 50px auto 30px auto;
    padding: 45px 30px;
    text-align: center;
    border-radius: 18px;
    background: rgba(128,128,128,0.08);
}

.welcome-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.welcome-title {
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 10px;
}

.welcome-text {
    color: #777;
    font-size: 15px;
    line-height: 1.6;
}

.attachment-card {
    padding: 10px 14px;
    border-radius: 10px;
    background: rgba(128,128,128,0.08);
    margin-bottom: 6px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

if "show_analytics" not in st.session_state:

    st.session_state.show_analytics = False


if "chats" not in st.session_state:

    st.session_state.chats = load_chats()


if "current_chat_id" not in st.session_state:

    if st.session_state.chats:

        st.session_state.current_chat_id = (
            st.session_state.chats[0]["id"]
        )

    else:

        first_chat = create_chat()

        st.session_state.chats = [
            first_chat
        ]

        st.session_state.current_chat_id = (
            first_chat["id"]
        )


if "search_text" not in st.session_state:

    st.session_state.search_text = ""


# ==================================================
# CURRENT CHAT
# ==================================================

current_chat = find_chat(
    st.session_state.chats,
    st.session_state.current_chat_id,
)


if current_chat is None:

    current_chat = create_chat()

    st.session_state.chats.insert(
        0,
        current_chat,
    )

    st.session_state.current_chat_id = (
        current_chat["id"]
    )


current_chat_id = current_chat["id"]


# ==================================================
# SOURCE RENDERER
# ==================================================

def render_source(
    source,
    source_number=None,
):
    """
    Render a clean source card.

    Supports both:
    - Global knowledge
    - Conversation files
    """

    if isinstance(
        source,
        dict,
    ):

        page_content = source.get(
            "page_content",
            "",
        )

        metadata = source.get(
            "metadata",
            {},
        )

    else:

        page_content = getattr(
            source,
            "page_content",
            "",
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


    page_content = str(
        page_content or ""
    ).strip()


    source_type = metadata.get(
        "source_type",
        "global_knowledge",
    )


    source_file = (
        metadata.get(
            "source_file"
        )
        or metadata.get(
            "file_name"
        )
        or metadata.get(
            "filename"
        )
    )


    if source_file:

        source_file = str(
            source_file
        ).strip()

        if (
            "\n" in source_file
            or len(source_file) > 180
        ):

            source_file = None


    source_title = (
        metadata.get(
            "section"
        )
        or ""
    )


    source_title = str(
        source_title
    ).strip()


    if not source_title:

        if page_content:

            first_line = (
                page_content
                .split(
                    "\n",
                    1,
                )[0]
                .strip()
            )

            prefixes = [
                "prompt:",
                "response:",
                "question:",
                "answer:",
            ]

            for prefix in prefixes:

                if first_line.lower().startswith(
                    prefix
                ):

                    first_line = (
                        first_line[
                            len(prefix):
                        ]
                        .strip()
                    )

            if (
                first_line
                and len(first_line) <= 120
            ):

                source_title = (
                    first_line
                )


    if not source_title:

        if source_file:

            source_title = (
                Path(
                    source_file
                ).stem
                .replace(
                    "_",
                    " ",
                )
                .replace(
                    "-",
                    " ",
                )
            )

        else:

            source_title = (
                "Knowledge Base Source"
            )


    if source_number is not None:

        st.markdown(
            f"**Source {source_number}**"
        )


    st.markdown(
        f"**{source_title}**"
    )


    location = metadata.get(
        "location"
    )


    if source_type == "conversation_file":

        if source_file:

            if location:

                st.caption(
                    f"📄 {Path(source_file).name} "
                    f"• {location}"
                )

            else:

                st.caption(
                    f"📄 {Path(source_file).name}"
                )

        else:

            st.caption(
                "📄 Conversation file"
            )

    else:

        st.caption(
            "📚 Knowledge Base"
        )


    st.markdown(
        "---"
    )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        "## 🤖 AI Customer Support"
    )


    # ----------------------------------------------
    # NEW CHAT
    # ----------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True,
    ):

        new_chat = create_chat()

        st.session_state.chats.insert(
            0,
            new_chat,
        )

        st.session_state.current_chat_id = (
            new_chat["id"]
        )

        st.session_state.show_analytics = (
            False
        )

        st.rerun()


    st.markdown(
        "---"
    )


    # ----------------------------------------------
    # DASHBOARD
    # ----------------------------------------------

    st.markdown(
        "### 📊 Dashboard"
    )


    if st.button(
        "📊 Analytics",
        use_container_width=True,
    ):

        st.session_state.show_analytics = (
            True
        )

        st.rerun()


    st.markdown(
        "---"
    )


    # ----------------------------------------------
    # SEARCH
    # ----------------------------------------------

    st.markdown(
        "### 🔎 Search Conversations"
    )


    search_text = st.text_input(
        "Search chats...",
        value=st.session_state.search_text,
        label_visibility="collapsed",
        placeholder="Search chats...",
    )


    st.session_state.search_text = (
        search_text
    )


    filtered_chats = search_chats(
        st.session_state.chats,
        search_text,
    )


    st.markdown(
        "---"
    )


    # ----------------------------------------------
    # CHAT HISTORY
    # ----------------------------------------------

    st.markdown(
        "### 💬 Chat History"
    )


    if not filtered_chats:

        st.caption(
            "No matching conversations."
        )

    else:

        for chat in filtered_chats:

            chat_id = chat["id"]

            title = chat.get(
                "title",
                "New Chat",
            )

            is_current = (
                chat_id
                == st.session_state.current_chat_id
            )

            button_label = (
                "🟢 "
                if is_current
                else "💬 "
            ) + title


            if st.button(
                button_label,
                key=f"chat_{chat_id}",
                use_container_width=True,
            ):

                st.session_state.current_chat_id = (
                    chat_id
                )

                st.session_state.show_analytics = (
                    False
                )

                st.rerun()


    st.markdown(
        "---"
    )


    # ----------------------------------------------
    # CHAT MANAGEMENT
    # ----------------------------------------------

    st.markdown(
        "### ⚙️ Chat Management"
    )


    rename_value = st.text_input(
        "Rename current chat",
        value=current_chat.get(
            "title",
            "New Chat",
        ),
        key="rename_input",
    )


    if st.button(
        "✏️ Rename Chat",
        use_container_width=True,
    ):

        rename_chat(
            current_chat,
            rename_value,
        )

        st.success(
            "Chat renamed."
        )

        st.rerun()


    if st.button(
        "🗑️ Delete Current Chat",
        use_container_width=True,
    ):

        deleted_chat_id = (
            current_chat["id"]
        )


        st.session_state.chats = delete_chat(
            st.session_state.chats,
            deleted_chat_id,
        )


        delete_conversation_files(
            deleted_chat_id
        )


        if st.session_state.chats:

            st.session_state.current_chat_id = (
                st.session_state.chats[0]["id"]
            )

        else:

            new_chat = create_chat()

            st.session_state.chats = [
                new_chat
            ]

            st.session_state.current_chat_id = (
                new_chat["id"]
            )


        st.rerun()


    if st.button(
        "🧹 Clear All Chats",
        use_container_width=True,
    ):

        chat_ids = [
            chat["id"]
            for chat in st.session_state.chats
        ]


        delete_all_chats()

        delete_all_conversation_files(
            chat_ids
        )


        new_chat = create_chat()

        st.session_state.chats = [
            new_chat
        ]

        st.session_state.current_chat_id = (
            new_chat["id"]
        )

        st.rerun()


    st.markdown(
        "---"
    )


    # ----------------------------------------------
    # ABOUT
    # ----------------------------------------------

    st.markdown(
        "### ℹ️ About"
    )


    st.write(
        """
        This AI Customer Support Assistant uses
        Retrieval-Augmented Generation (RAG) to
        answer questions from trusted knowledge
        sources and files attached to the current
        conversation.
        """
    )


    # ----------------------------------------------
    # TECH STACK
    # ----------------------------------------------

    st.markdown(
        "### 🛠️ Tech Stack"
    )


    st.write(
        """
        Python • Streamlit • LangChain • Gemini
        • HuggingFace Embeddings • FAISS • SQLite
        """
    )


# ==================================================
# ANALYTICS
# ==================================================

if st.session_state.show_analytics:

    st.markdown(
        '<div class="title">📊 Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="subtitle">Overview of your customer support conversations</div>',
        unsafe_allow_html=True,
    )


    total_chats = len(
        st.session_state.chats
    )


    total_messages = sum(
        len(
            chat.get(
                "messages",
                [],
            )
        )
        for chat in st.session_state.chats
    )


    total_user_messages = sum(
        sum(
            1
            for message in chat.get(
                "messages",
                [],
            )
            if message.get(
                "role"
            ) == "user"
        )
        for chat in st.session_state.chats
    )


    total_assistant_messages = sum(
        sum(
            1
            for message in chat.get(
                "messages",
                [],
            )
            if message.get(
                "role"
            ) == "assistant"
        )
        for chat in st.session_state.chats
    )


    feedback_positive = 0

    feedback_negative = 0


    for chat in st.session_state.chats:

        for message in chat.get(
            "messages",
            [],
        ):

            feedback = message.get(
                "feedback"
            )

            if feedback == "positive":

                feedback_positive += 1

            elif feedback == "negative":

                feedback_negative += 1


    metric_col1, metric_col2, metric_col3, metric_col4 = (
        st.columns(4)
    )


    with metric_col1:

        st.metric(
            "Total Chats",
            total_chats,
        )


    with metric_col2:

        st.metric(
            "Total Messages",
            total_messages,
        )


    with metric_col3:

        st.metric(
            "Questions Asked",
            total_user_messages,
        )


    with metric_col4:

        st.metric(
            "AI Responses",
            total_assistant_messages,
        )


    st.markdown(
        "---"
    )


    feedback_col1, feedback_col2, feedback_col3 = (
        st.columns(3)
    )


    with feedback_col1:

        st.metric(
            "👍 Positive Feedback",
            feedback_positive,
        )


    with feedback_col2:

        st.metric(
            "👎 Negative Feedback",
            feedback_negative,
        )


    with feedback_col3:

        total_feedback = (
            feedback_positive
            + feedback_negative
        )

        st.metric(
            "Total Feedback",
            total_feedback,
        )


    st.markdown(
        "---"
    )


    st.markdown(
        "### 💬 Recent Conversations"
    )


    if not st.session_state.chats:

        st.info(
            "No conversations available yet."
        )

    else:

        for chat in st.session_state.chats[:10]:

            title = chat.get(
                "title",
                "New Chat",
            )

            messages = chat.get(
                "messages",
                [],
            )

            user_count = sum(
                1
                for message in messages
                if message.get(
                    "role"
                ) == "user"
            )

            assistant_count = sum(
                1
                for message in messages
                if message.get(
                    "role"
                ) == "assistant"
            )


            with st.container():

                st.markdown(
                    f"**💬 {title}**"
                )

                st.caption(
                    f"{user_count} questions • "
                    f"{assistant_count} AI responses"
                )


    st.markdown(
        "---"
    )


    if st.button(
        "← Back to Chat",
        use_container_width=True,
    ):

        st.session_state.show_analytics = (
            False
        )

        st.rerun()


    st.stop()


# ==================================================
# MAIN HEADER
# ==================================================

st.markdown(
    '<div class="title">🤖 AI Customer Service Assistant</div>',
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="subtitle">Ask questions, attach files, and get answers grounded in trusted information.</div>',
    unsafe_allow_html=True,
)


# ==================================================
# WELCOME
# ==================================================

if not current_chat["messages"]:

    st.markdown(
        """
        <div class="welcome-box">

            <div class="welcome-icon">
                💬
            </div>

            <div class="welcome-title">
                How can I help you?
            </div>

            <div class="welcome-text">
                Ask me a question or attach a document
                and I can answer using information from
                your conversation files and available
                knowledge.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# SUGGESTIONS
# ==================================================

if not current_chat["messages"]:

    st.markdown(
        "### 💡 Try asking"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🎓 Do you provide internships?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "Do you provide internships?"
            )

            st.rerun()


        if st.button(
            "📚 What courses are available?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "What courses are available?"
            )

            st.rerun()


    with col2:

        if st.button(
            "💻 Can I learn Power BI on Mac?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "Can I learn Power BI on Mac?"
            )

            st.rerun()


        if st.button(
            "🎯 What are the eligibility requirements?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "What are the eligibility requirements?"
            )

            st.rerun()


# ==================================================
# DISPLAY ATTACHED FILES
# ==================================================

conversation_files = list_conversation_files(
    current_chat_id
)


if conversation_files:

    st.markdown(
        "### 📎 Attached files"
    )


    for file_record in conversation_files:

        file_col1, file_col2 = st.columns(
            [8, 1]
        )


        with file_col1:

            file_name = file_record.get(
                "file_name",
                "Uploaded file",
            )

            file_size = file_record.get(
                "size_display",
                "",
            )

            chunk_count = file_record.get(
                "chunk_count",
                0,
            )

            st.markdown(
                f"""
                <div class="attachment-card">
                    📄 <strong>{file_name}</strong>
                    <br>
                    <small>
                        {file_size}
                        • {chunk_count} searchable chunks
                    </small>
                </div>
                """,
                unsafe_allow_html=True,
            )


        with file_col2:

            if st.button(
                "×",
                key=f"remove_file_{current_chat_id}_{file_record['id']}",
                help=f"Remove {file_name}",
            ):

                with st.spinner(
                    "Removing file..."
                ):

                    remove_conversation_file(
                        current_chat_id,
                        file_record["id"],
                    )

                st.rerun()


# ==================================================
# CHAT DISPLAY
# ==================================================

for index, message in enumerate(
    current_chat["messages"]
):

    role = message.get(
        "role",
        "assistant",
    )


    content = message.get(
        "content",
        "",
    )


    with st.chat_message(role):

        st.markdown(
            content
        )


        if role == "assistant":

            sources = message.get(
                "sources",
                [],
            )


            button_col1, button_col2, button_col3, button_col4 = (
                st.columns(
                    [1, 1, 1, 1]
                )
            )


            # ------------------------------------------
            # COPY
            # ------------------------------------------

            with button_col1:

                if st.button(
                    "📋",
                    key=f"copy_{index}",
                    help="Copy response",
                ):

                    components.html(
                        f"""
                        <script>
                        navigator.clipboard.writeText(
                            {content!r}
                        );
                        </script>
                        """,
                        height=0,
                    )


                    st.toast(
                        "Response copied!"
                    )


            # ------------------------------------------
            # REGENERATE
            # ------------------------------------------

            with button_col2:

                if st.button(
                    "🔄",
                    key=f"regen_{index}",
                    help="Regenerate response",
                ):

                    previous_question = None


                    for previous_message in reversed(
                        current_chat["messages"][:index]
                    ):

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

                            break


                    if previous_question:

                        del current_chat[
                            "messages"
                        ][index]


                        st.session_state.pending_question = (
                            previous_question
                        )


                        st.rerun()


            # ------------------------------------------
            # POSITIVE
            # ------------------------------------------

            with button_col3:

                if st.button(
                    "👍",
                    key=f"positive_{index}",
                    help="Helpful",
                ):

                    update_message_feedback(
                        current_chat,
                        index,
                        "positive",
                    )


                    st.toast(
                        "Thanks for your feedback!"
                    )


                    st.rerun()


            # ------------------------------------------
            # NEGATIVE
            # ------------------------------------------

            with button_col4:

                if st.button(
                    "👎",
                    key=f"negative_{index}",
                    help="Not helpful",
                ):

                    update_message_feedback(
                        current_chat,
                        index,
                        "negative",
                    )


                    st.toast(
                        "Thanks for your feedback!"
                    )


                    st.rerun()


            # ------------------------------------------
            # SOURCES
            # ------------------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):

                        render_source(
                            source,
                            source_number,
                        )


# ==================================================
# PROCESS QUESTION
# ==================================================

def process_question(
    question,
):

    if not isinstance(
        question,
        str,
    ):
        return


    question = question.strip()


    if not question:
        return


    # ----------------------------------------------
    # SAVE USER MESSAGE
    # ----------------------------------------------

    add_message(
        current_chat,
        "user",
        question,
    )


    start_time = time.perf_counter()


    try:

        with st.chat_message(
            "assistant"
        ):

            stream, sources = get_qa_stream(
                question,
                chat_history=current_chat[
                    "messages"
                ][:-1],
                chat_id=current_chat_id,
            )


            st.markdown(
                '<div style="margin-bottom: 8px;"></div>',
                unsafe_allow_html=True,
            )


            answer = st.write_stream(
                stream
            )


            if answer is None:

                answer = ""


            elif not isinstance(
                answer,
                str,
            ):

                answer = str(
                    answer
                )


            answer = answer.strip()


            elapsed_time = (
                time.perf_counter()
                - start_time
            )


            # ------------------------------------------
            # SOURCES
            # ------------------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):

                        render_source(
                            source,
                            source_number,
                        )


        # ------------------------------------------
        # SAVE RESPONSE
        # ------------------------------------------

        add_message(
            current_chat,
            "assistant",
            answer,
            sources=sources,
            response_time=elapsed_time,
        )


    except Exception as error:

        error_message = str(
            error
        )


        elapsed_time = (
            time.perf_counter()
            - start_time
        )


        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED"
            in error_message
        ):

            answer = (
                "⚠️ **AI service temporarily unavailable**\n\n"
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )

        else:

            answer = (
                "⚠️ **Something went wrong while "
                "processing your request.**\n\n"
                "Please try again."
            )


        add_message(
            current_chat,
            "assistant",
            answer,
            response_time=elapsed_time,
        )


        st.error(
            answer
        )


# ==================================================
# PENDING QUESTION
# ==================================================

if "pending_question" in st.session_state:

    pending_question = (
        st.session_state.pop(
            "pending_question",
            None,
        )
    )


    if (
        isinstance(
            pending_question,
            str,
        )
        and pending_question.strip()
    ):

        process_question(
            pending_question
        )

        st.rerun()


# ==================================================
# FILE UPLOADER
# ==================================================

st.markdown(
    "---"
)


st.markdown(
    "### 📎 Attach files"
)


uploaded_files = st.file_uploader(
    "Attach files to this conversation",
    type=[
        "pdf",
        "docx",
        "txt",
        "csv",
    ],
    accept_multiple_files=True,
    label_visibility="collapsed",
    help=(
        "Files are automatically processed and "
        "made available to this conversation."
    ),
)


# ==================================================
# AUTOMATIC FILE PROCESSING
# ==================================================

if uploaded_files:

    upload_signature = (
        get_attachment_signature(
            uploaded_files
        )
    )


    session_key = (
        f"processed_upload_{current_chat_id}"
    )


    previous_signature = st.session_state.get(
        session_key,
        "",
    )


    if upload_signature != previous_signature:

        st.session_state[
            session_key
        ] = upload_signature


        with st.spinner(
            "Processing files..."
        ):

            result = add_conversation_files(
                current_chat_id,
                uploaded_files,
            )


        added_files = result.get(
            "added",
            [],
        )

        skipped_files = result.get(
            "skipped",
            [],
        )

        errors = result.get(
            "errors",
            [],
        )


        if added_files:

            for file_record in added_files:

                st.success(
                    f"📄 {file_record['file_name']} "
                    f"is ready to use."
                )


        for skipped_file in skipped_files:

            st.info(
                f"📄 {skipped_file['name']} "
                f"is already attached."
            )


        for error in errors:

            st.error(
                error
            )


        if added_files:

            st.rerun()


# ==================================================
# CHAT INPUT
# ==================================================

user_question = st.chat_input(
    "Ask me anything..."
)


if user_question:

    process_question(
        user_question
    )

    st.rerun()