import logging

import streamlit as st
import streamlit.components.v1 as components

from chat_manager import (
    add_message,
    create_chat,
    delete_chat,
    find_chat,
    rename_chat,
)

from config import (
    ERROR_MESSAGES,
    PAGE_CONFIG,
    SESSION_STATE_KEYS,
    SUGGESTED_QUESTIONS,
    SUCCESS_MESSAGES,
    WELCOME_MESSAGE,
    WELCOME_SUBTEXT,
)

from langchain_helper import (
    create_vector_db,
    get_qa_chain,
)


logger = logging.getLogger(__name__)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(**PAGE_CONFIG)


# ============================================================================
# STYLING
# ============================================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .welcome {
        text-align: center;
        padding: 2rem;
        margin: 1rem 0 2rem 0;
        border-radius: 15px;
        background: rgba(128, 128, 128, 0.08);
    }

    .welcome-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .welcome-title {
        font-size: 1.4rem;
        font-weight: 600;
    }

    .welcome-text {
        color: #777;
        margin-top: 0.5rem;
    }

    .footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# SESSION STATE
# ============================================================================

if "chats" not in st.session_state:
    st.session_state.chats = []


if "current_chat_id" not in st.session_state:

    new_chat = create_chat()

    st.session_state.chats.append(
        new_chat
    )

    st.session_state.current_chat_id = (
        new_chat["id"]
    )


for key in SESSION_STATE_KEYS:

    if key not in st.session_state:
        st.session_state[key] = []


if "feedback" not in st.session_state:
    st.session_state.feedback = {}


# ============================================================================
# CHAT HELPERS
# ============================================================================

def get_current_chat():
    """Return the currently selected conversation."""

    return find_chat(
        st.session_state.chats,
        st.session_state.current_chat_id,
    )


def start_new_chat():
    """Create and select a new conversation."""

    chat = create_chat()

    st.session_state.chats.insert(
        0,
        chat,
    )

    st.session_state.current_chat_id = (
        chat["id"]
    )

    st.session_state.messages = []
    st.session_state.sources = []


def select_chat(chat_id):
    """Select an existing conversation."""

    st.session_state.current_chat_id = chat_id

    chat = find_chat(
        st.session_state.chats,
        chat_id,
    )

    if chat:

        st.session_state.messages = (
            chat["messages"]
        )

        st.session_state.sources = [
            message.get("sources", [])
            for message in chat["messages"]
            if message["role"] == "assistant"
        ]


def clear_current_chat():
    """Clear messages from the current conversation."""

    chat = get_current_chat()

    if chat:

        chat["messages"] = []
        chat["title"] = "New Chat"

    st.session_state.messages = []
    st.session_state.sources = []


def remove_chat(chat_id):
    """Delete a conversation."""

    st.session_state.chats = delete_chat(
        st.session_state.chats,
        chat_id,
    )

    if not st.session_state.chats:

        chat = create_chat()

        st.session_state.chats.append(
            chat
        )

    st.session_state.current_chat_id = (
        st.session_state.chats[0]["id"]
    )

    select_chat(
        st.session_state.current_chat_id
    )


# ============================================================================
# SOURCE HELPERS
# ============================================================================

def extract_source_information(source):
    """Extract question and answer from a source document."""

    question = ""
    answer = ""

    for line in source.page_content.split("\n"):

        if line.lower().startswith("prompt:"):

            question = line.split(
                ":",
                1,
            )[1].strip()

        elif line.lower().startswith("response:"):

            answer = line.split(
                ":",
                1,
            )[1].strip()

    return question, answer


def render_sources(sources):
    """Display retrieved knowledge-base sources."""

    if not sources:
        return

    with st.expander(
        "📚 View Source Information"
    ):

        for source in sources:

            question, answer = (
                extract_source_information(
                    source
                )
            )

            if question:

                st.markdown(
                    f"**Question:** {question}"
                )

            if answer:

                st.markdown(
                    f"**Answer:** {answer}"
                )

            st.markdown("---")


# ============================================================================
# COPY BUTTON
# ============================================================================

def render_copy_button(message_id, content):
    """Render a compact browser-based copy button."""

    safe_content = (
        content
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
        .replace("</script>", "<\\/script>")
    )

    components.html(
        f"""
        <button
            onclick="
                navigator.clipboard.writeText(`{safe_content}`);
                this.innerText = '✓ Copied';
                setTimeout(() => {{
                    this.innerText = '📋 Copy';
                }}, 1500);
            "
            style="
                width: 100%;
                height: 32px;
                border: 1px solid rgba(128,128,128,0.35);
                border-radius: 7px;
                background: transparent;
                cursor: pointer;
                font-size: 13px;
                white-space: nowrap;
                padding: 0 8px;
            "
        >
            📋 Copy
        </button>
        """,
        height=36,
        scrolling=False,
    )


# ============================================================================
# FEEDBACK
# ============================================================================

def give_feedback(message_id, value):
    """Store user feedback for an assistant response."""

    st.session_state.feedback[message_id] = value

    logger.info(
        "Feedback recorded: %s -> %s",
        message_id,
        value,
    )


# ============================================================================
# REGENERATE RESPONSE
# ============================================================================

def regenerate_response(message_index):
    """Regenerate an existing assistant response."""

    chat = get_current_chat()

    if not chat:
        return

    if message_index <= 0:
        return

    assistant_message = chat["messages"][message_index]

    if assistant_message["role"] != "assistant":
        return

    user_message = None
    user_index = None

    for index in range(
        message_index - 1,
        -1,
        -1,
    ):

        if chat["messages"][index]["role"] == "user":

            user_message = chat["messages"][index]
            user_index = index

            break

    if user_message is None:
        return

    previous_messages = (
        chat["messages"][:user_index]
    )

    try:

        _, stream_chain = get_qa_chain()

        full_answer = ""
        sources = []

        response_area = st.empty()

        with st.spinner(
            "Regenerating response..."
        ):

            stream = stream_chain(
                user_message["content"],
                chat_history=previous_messages,
            )

            for event in stream:

                if event["type"] == "token":

                    full_answer += event["content"]

                    response_area.markdown(
                        full_answer + "▌"
                    )

                elif event["type"] == "sources":

                    sources = event.get(
                        "source_documents",
                        [],
                    )

        response_area.markdown(
            full_answer
        )

        assistant_message["content"] = (
            full_answer
        )

        assistant_message["sources"] = (
            sources
        )

        st.session_state.messages = (
            chat["messages"]
        )

        logger.info(
            "Response regenerated successfully"
        )

        st.rerun()

    except Exception as error:

        display_error(error)


# ============================================================================
# ERROR HANDLING
# ============================================================================

def display_error(error):
    """Display a user-friendly error message."""

    error_message = str(error)

    logger.error(
        "Error processing request: %s",
        error_message,
        exc_info=True,
    )

    if (
        "429" in error_message
        or "RESOURCE_EXHAUSTED" in error_message
    ):

        st.warning(
            ERROR_MESSAGES["api_rate_limit"]
        )

    elif (
        "503" in error_message
        or "UNAVAILABLE" in error_message
    ):

        st.warning(
            "⚠️ Gemini is temporarily unavailable. "
            "Please try again in a moment."
        )

    else:

        st.error(
            ERROR_MESSAGES["generic_error"]
        )


# ============================================================================
# QUESTION PROCESSING
# ============================================================================

def process_question(question):
    """Process a user question using streaming RAG."""

    question = question.strip()

    if not question:
        return

    chat = get_current_chat()

    if not chat:

        start_new_chat()

        chat = get_current_chat()

    logger.info(
        "Processing question: %s",
        question[:80],
    )

    previous_messages = (
        chat["messages"].copy()
    )

    add_message(
        chat,
        "user",
        question,
    )

    st.session_state.messages = (
        chat["messages"]
    )

    try:

        _, stream_chain = get_qa_chain()

        response_area = st.empty()

        full_answer = ""
        sources = []

        with st.spinner(
            "Searching knowledge base..."
        ):

            stream = stream_chain(
                question,
                chat_history=previous_messages,
            )

            for event in stream:

                if event["type"] == "token":

                    full_answer += event["content"]

                    response_area.markdown(
                        full_answer + "▌"
                    )

                elif event["type"] == "sources":

                    sources = event.get(
                        "source_documents",
                        [],
                    )

        response_area.markdown(
            full_answer
        )

        add_message(
            chat,
            "assistant",
            full_answer,
            sources,
        )

        st.session_state.messages = (
            chat["messages"]
        )

        st.session_state.sources = [
            message.get("sources", [])
            for message in chat["messages"]
            if message["role"] == "assistant"
        ]

        logger.info(
            "Answer generated with %d sources",
            len(sources),
        )

    except Exception as error:

        display_error(error)


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:

    st.title("🤖 AI Customer Support")

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        start_new_chat()

        st.rerun()

    st.markdown("---")

    st.markdown("### 💬 Chat History")

    if not st.session_state.chats:

        st.caption(
            "No conversations yet."
        )

    for chat in st.session_state.chats:

        is_current = (
            chat["id"]
            == st.session_state.current_chat_id
        )

        label = chat["title"]

        if is_current:

            label = f"👉 {label}"

        if st.button(
            label,
            key=f"chat_{chat['id']}",
            use_container_width=True,
        ):

            select_chat(
                chat["id"]
            )

            st.rerun()

    st.markdown("---")

    current_chat = get_current_chat()

    if current_chat:

        st.markdown(
            "### ⚙️ Chat Settings"
        )

        rename_value = st.text_input(
            "Rename conversation",
            value=current_chat["title"],
            key=f"rename_{current_chat['id']}",
        )

        if st.button(
            "✏️ Rename Chat",
            use_container_width=True,
        ):

            rename_chat(
                current_chat,
                rename_value,
            )

            st.rerun()

        if st.button(
            "🗑️ Delete Chat",
            use_container_width=True,
        ):

            remove_chat(
                current_chat["id"]
            )

            st.rerun()

        if st.button(
            "🧹 Clear Messages",
            use_container_width=True,
        ):

            clear_current_chat()

            st.rerun()

    st.markdown("---")

    st.markdown("### 📚 Knowledge Base")

    if st.button(
        "🔄 Create / Update Knowledge Base",
        use_container_width=True,
    ):

        logger.info(
            "User requested knowledge base update"
        )

        try:

            with st.spinner(
                "Updating knowledge base..."
            ):

                create_vector_db()

            st.success(
                SUCCESS_MESSAGES["kb_created"]
            )

        except Exception as error:

            display_error(error)

    st.success(
        "🟢 Knowledge Base Ready"
    )

    st.markdown("---")

    st.markdown("### ℹ️ About")

    st.write(
        """
        This chatbot uses Retrieval-Augmented Generation (RAG)
        to answer customer service questions using information
        from the available knowledge base.
        """
    )

    st.markdown("### 🛠️ Tech Stack")

    st.write(
        """
        - Python
        - Streamlit
        - LangChain
        - Gemini
        - HuggingFace Embeddings
        - FAISS
        """
    )


# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown(
    '<div class="title">🤖 AI Customer Service Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions and get answers from our knowledge base'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================================
# CURRENT CHAT
# ============================================================================

current_chat = get_current_chat()

messages = (
    current_chat["messages"]
    if current_chat
    else []
)


# ============================================================================
# WELCOME SCREEN
# ============================================================================

if not messages:

    st.markdown(
        f"""
        <div class="welcome">
            <div class="welcome-icon">💬</div>
            <div class="welcome-title">{WELCOME_MESSAGE}</div>
            <p class="welcome-text">{WELCOME_SUBTEXT}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    columns = [
        col1,
        col2,
    ]

    for question in SUGGESTED_QUESTIONS:

        with columns[question["col"]]:

            if st.button(
                f"{question['emoji']} {question['text']}",
                use_container_width=True,
            ):

                process_question(
                    question["text"]
                )

                st.rerun()


# ============================================================================
# MESSAGE DISPLAY
# ============================================================================

for message_index, message in enumerate(messages):

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            message_id = (
                f"{current_chat['id']}_{message_index}"
            )

            st.markdown(
                "<div style='height: 2px'></div>",
                unsafe_allow_html=True,
            )

            action_col1, action_col2, action_col3, action_col4, action_space = (
                st.columns(
                    [1.25, 1.65, 0.55, 0.55, 5.5]
                )
            )

            with action_col1:

                render_copy_button(
                    message_id,
                    message["content"],
                )

            with action_col2:

                if st.button(
                    "🔄 Regenerate",
                    key=f"regenerate_{message_id}",
                ):

                    regenerate_response(
                        message_index
                    )

            with action_col3:

                if st.button(
                    "👍",
                    key=f"thumb_up_{message_id}",
                ):

                    give_feedback(
                        message_id,
                        "positive",
                    )

                    st.rerun()

            with action_col4:

                if st.button(
                    "👎",
                    key=f"thumb_down_{message_id}",
                ):

                    give_feedback(
                        message_id,
                        "negative",
                    )

                    st.rerun()

            if message_id in st.session_state.feedback:

                feedback_value = (
                    st.session_state.feedback[
                        message_id
                    ]
                )

                if feedback_value == "positive":

                    st.caption(
                        "👍 Thanks for your feedback!"
                    )

                else:

                    st.caption(
                        "Thanks for your feedback. "
                        "We'll use it to improve the assistant."
                    )

            render_sources(
                message.get(
                    "sources",
                    [],
                )
            )


# ============================================================================
# CHAT INPUT
# ============================================================================

user_question = st.chat_input(
    "Ask me anything about our services..."
)


if user_question:

    with st.chat_message("user"):

        st.markdown(
            user_question
        )

    with st.chat_message("assistant"):

        process_question(
            user_question
        )

    st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

st.markdown(
    """
    <div class="footer">
        Built with Python, Streamlit, LangChain, Gemini,
        HuggingFace & FAISS
    </div>
    """,
    unsafe_allow_html=True,
)