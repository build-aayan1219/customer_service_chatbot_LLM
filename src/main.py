import logging

import streamlit as st

from langchain_helper import create_vector_db, get_qa_chain
from config import (
    PAGE_CONFIG,
    SUGGESTED_QUESTIONS,
    WELCOME_MESSAGE,
    WELCOME_SUBTEXT,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    SESSION_STATE_KEYS,
)
from chat_manager import (
    create_chat,
    add_message,
    find_chat,
    delete_chat,
    rename_chat,
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

    .chat-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
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
    chat = create_chat()
    st.session_state.chats.append(chat)
    st.session_state.current_chat_id = chat["id"]

for key in SESSION_STATE_KEYS:
    if key not in st.session_state:
        st.session_state[key] = []


# ============================================================================
# CHAT HELPERS
# ============================================================================

def get_current_chat():
    return find_chat(
        st.session_state.chats,
        st.session_state.current_chat_id,
    )


def start_new_chat():
    chat = create_chat()

    st.session_state.chats.insert(0, chat)
    st.session_state.current_chat_id = chat["id"]

    st.session_state.messages = []
    st.session_state.sources = []


def select_chat(chat_id):
    st.session_state.current_chat_id = chat_id

    chat = find_chat(
        st.session_state.chats,
        chat_id,
    )

    if chat:
        st.session_state.messages = chat["messages"]
        st.session_state.sources = [
            message.get("sources", [])
            for message in chat["messages"]
            if message["role"] == "assistant"
        ]


def clear_current_chat():
    chat = get_current_chat()

    if chat:
        chat["messages"] = []
        chat["title"] = "New Chat"

    st.session_state.messages = []
    st.session_state.sources = []


def remove_chat(chat_id):
    st.session_state.chats = delete_chat(
        st.session_state.chats,
        chat_id,
    )

    if not st.session_state.chats:
        chat = create_chat()
        st.session_state.chats.append(chat)

    st.session_state.current_chat_id = st.session_state.chats[0]["id"]

    select_chat(st.session_state.current_chat_id)


# ============================================================================
# SOURCE HELPERS
# ============================================================================

def extract_source_information(source):
    question = ""
    answer = ""

    for line in source.page_content.split("\n"):
        if line.lower().startswith("prompt:"):
            question = line.split(":", 1)[1].strip()

        elif line.lower().startswith("response:"):
            answer = line.split(":", 1)[1].strip()

    return question, answer


def render_sources(sources):
    if not sources:
        return

    with st.expander("📚 View Source Information"):
        for source in sources:
            question, answer = extract_source_information(source)

            if question:
                st.markdown(f"**Question:** {question}")

            if answer:
                st.markdown(f"**Answer:** {answer}")

            st.markdown("---")


# ============================================================================
# ERROR HANDLING
# ============================================================================

def display_error(error):
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
        st.warning(ERROR_MESSAGES["api_rate_limit"])

    elif (
        "503" in error_message
        or "UNAVAILABLE" in error_message
    ):
        st.warning(
            "⚠️ Gemini is temporarily unavailable. "
            "Please try again in a moment."
        )

    else:
        st.error(ERROR_MESSAGES["generic_error"])


# ============================================================================
# QUESTION PROCESSING
# ============================================================================

def process_question(question):
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

    add_message(
        chat,
        "user",
        question,
    )

    st.session_state.messages = chat["messages"]

    try:
        with st.spinner("Thinking..."):
            chain = get_qa_chain()
            response = chain(question)

        answer = response["result"]
        sources = response.get("source_documents", [])

        add_message(
            chat,
            "assistant",
            answer,
            sources,
        )

        st.session_state.messages = chat["messages"]
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
        st.caption("No conversations yet.")

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
            select_chat(chat["id"])
            st.rerun()

    st.markdown("---")

    current_chat = get_current_chat()

    if current_chat:

        st.markdown("### ⚙️ Chat Settings")

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
            remove_chat(current_chat["id"])
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
        logger.info("User requested knowledge base update")

        try:
            with st.spinner("Updating knowledge base..."):
                create_vector_db()

            st.success(
                SUCCESS_MESSAGES["kb_created"]
            )

        except Exception as error:
            display_error(error)

    st.success("🟢 Knowledge Base Ready")

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
            <div class="welcome-title">
                {WELCOME_MESSAGE}
            </div>
            <div class="welcome-text">
                {WELCOME_SUBTEXT}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    columns = [col1, col2]

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

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            render_sources(
                message.get("sources", [])
            )


# ============================================================================
# CHAT INPUT
# ============================================================================

user_question = st.chat_input(
    "Ask me anything about our services..."
)

if user_question:

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        process_question(user_question)

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