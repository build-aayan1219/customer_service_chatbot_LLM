import sys
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from src.analytics import render_analytics
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
from src.knowledge_base import render_knowledge_base
from src.langchain_helper import get_qa_chain


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False

if "show_knowledge_base" not in st.session_state:
    st.session_state.show_knowledge_base = False

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "search_text" not in st.session_state:
    st.session_state.search_text = ""


# ============================================================
# GLOBAL CSS
#
# IMPORTANT:
# This is the ONLY custom CSS block.
# It explicitly uses unsafe_allow_html=True.
#
# No welcome HTML is used anywhere below.
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .main-subtitle {
            color: #777;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        .welcome-container {
            max-width: 700px;
            margin: 50px auto 30px auto;
            padding: 45px 30px;
            text-align: center;
            border-radius: 18px;
            background: rgba(128, 128, 128, 0.08);
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
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHAT INITIALIZATION
# ============================================================

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


# ============================================================
# ANALYTICS ROUTE
# ============================================================

if st.session_state.show_analytics:

    with st.sidebar:

        st.markdown(
            "## 🤖 AI Customer Support"
        )

        st.caption(
            "Analytics & Monitoring"
        )

        st.markdown("---")

        if st.button(
            "← Back to Chat",
            use_container_width=True,
            key="back_from_analytics",
        ):

            st.session_state.show_analytics = False

            st.rerun()

        st.markdown("---")

        st.success(
            "📊 Analytics Active"
        )

    render_analytics()

    st.stop()


# ============================================================
# KNOWLEDGE BASE ROUTE
# ============================================================

if st.session_state.show_knowledge_base:

    with st.sidebar:

        st.markdown(
            "## 🤖 AI Customer Support"
        )

        st.caption(
            "Knowledge Base Manager"
        )

        st.markdown("---")

        if st.button(
            "← Back to Chat",
            use_container_width=True,
            key="back_from_knowledge_base",
        ):

            st.session_state.show_knowledge_base = False

            st.rerun()

        st.markdown("---")

        st.success(
            "📚 Knowledge Base Active"
        )

    render_knowledge_base()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🤖 AI Customer Support"
    )

    st.markdown("")

    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True,
        key="new_chat_button",
    ):

        new_chat = create_chat()

        st.session_state.chats.insert(
            0,
            new_chat,
        )

        st.session_state.current_chat_id = (
            new_chat["id"]
        )

        st.session_state.pending_question = None

        st.rerun()

    st.markdown("---")


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Dashboard"
    )

    if st.button(
        "📊 Analytics",
        use_container_width=True,
        key="analytics_button",
    ):

        st.session_state.show_analytics = True
        st.session_state.show_knowledge_base = False

        st.rerun()


    if st.button(
        "📚 Knowledge Base",
        use_container_width=True,
        key="knowledge_base_button",
    ):

        st.session_state.show_knowledge_base = True
        st.session_state.show_analytics = False

        st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # SEARCH CONVERSATIONS
    # --------------------------------------------------------

    st.markdown(
        "### 🔎 Search Conversations"
    )

    search_text = st.text_input(
        "Search chats...",
        value=st.session_state.search_text,
        label_visibility="collapsed",
        placeholder="Search chats...",
        key="conversation_search",
    )

    st.session_state.search_text = search_text

    filtered_chats = search_chats(
        st.session_state.chats,
        search_text,
    )

    st.markdown("---")


    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

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

                st.session_state.pending_question = None

                st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # CHAT MANAGEMENT
    # --------------------------------------------------------

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
        key="rename_chat_button",
    ):

        cleaned_name = rename_value.strip()

        if cleaned_name:

            rename_chat(
                current_chat,
                cleaned_name,
            )

            st.success(
                "Chat renamed."
            )

            st.rerun()

        else:

            st.warning(
                "Chat name cannot be empty."
            )


    if st.button(
        "🗑️ Delete Current Chat",
        use_container_width=True,
        key="delete_current_chat_button",
    ):

        st.session_state.chats = delete_chat(
            st.session_state.chats,
            current_chat["id"],
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
        key="clear_all_chats_button",
    ):

        delete_all_chats()

        new_chat = create_chat()

        st.session_state.chats = [
            new_chat
        ]

        st.session_state.current_chat_id = (
            new_chat["id"]
        )

        st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # KNOWLEDGE BASE STATUS
    # --------------------------------------------------------

    st.markdown(
        "### 📚 Knowledge Base"
    )

    if st.button(
        "🔄 Create / Update Knowledge Base",
        use_container_width=True,
        key="update_kb_button",
    ):

        try:

            from src.langchain_helper import (
                create_vector_db
            )

            with st.spinner(
                "Updating knowledge base..."
            ):

                create_vector_db()

            st.success(
                "Knowledge base updated successfully!"
            )

        except Exception as error:

            error_message = str(error)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED"
                in error_message
            ):

                st.warning(
                    "Gemini API usage limit has "
                    "been reached. The knowledge "
                    "base itself may still be updated."
                )

            else:

                st.error(
                    "Could not update the knowledge base."
                )


    st.success(
        "🟢 Knowledge Base Ready"
    )

    st.markdown("---")


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.markdown(
        "### ℹ️ About"
    )

    st.write(
        "This AI Customer Support Assistant "
        "uses Retrieval-Augmented Generation "
        "(RAG) to answer questions using the "
        "available knowledge base."
    )


    # --------------------------------------------------------
    # TECH STACK
    # --------------------------------------------------------

    st.markdown(
        "### 🛠️ Tech Stack"
    )

    st.write(
        "Python • Streamlit • LangChain • Gemini "
        "• HuggingFace Embeddings • FAISS • SQLite"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🤖 AI Customer Service Assistant
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-subtitle">
        Ask questions and get answers from our knowledge base
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME SCREEN
#
# IMPORTANT:
# NO RAW HTML IS USED HERE.
#
# The previous problem happened because the welcome HTML
# was being rendered as text.
#
# This version uses Streamlit-native components only.
# ============================================================

if not current_chat.get("messages"):

    welcome_container = st.container()

    with welcome_container:

        st.markdown("")

        st.markdown(
            "### 💬"
        )

        st.markdown(
            "## How can I help you?"
        )

        st.markdown(
            "Ask me about courses, internships, "
            "services, tools and other available "
            "information."
        )

        st.markdown("")


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

if not current_chat.get("messages"):

    st.markdown(
        "### 💡 Try asking"
    )

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🎓 Do you provide internships?",
            use_container_width=True,
            key="suggestion_internship",
        ):

            st.session_state.pending_question = (
                "Do you provide internships?"
            )

            st.rerun()


        if st.button(
            "📚 What courses are available?",
            use_container_width=True,
            key="suggestion_courses",
        ):

            st.session_state.pending_question = (
                "What courses are available?"
            )

            st.rerun()


    with col2:

        if st.button(
            "💻 Can I learn Power BI on Mac?",
            use_container_width=True,
            key="suggestion_powerbi",
        ):

            st.session_state.pending_question = (
                "Can I learn Power BI on Mac?"
            )

            st.rerun()


        if st.button(
            "🎯 What are the eligibility requirements?",
            use_container_width=True,
            key="suggestion_eligibility",
        ):

            st.session_state.pending_question = (
                "What are the eligibility requirements?"
            )

            st.rerun()


# ============================================================
# DISPLAY EXISTING CHAT
# ============================================================

for index, message in enumerate(
    current_chat.get("messages", [])
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

        # ----------------------------------------------------
        # IMPORTANT:
        # AI responses are rendered as Markdown.
        #
        # We DO NOT use unsafe_allow_html=True here.
        # Therefore an AI response containing HTML tags
        # will not become arbitrary page HTML.
        # ----------------------------------------------------

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


            # ------------------------------------------------
            # COPY
            # ------------------------------------------------

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


            # ------------------------------------------------
            # REGENERATE
            # ------------------------------------------------

            with button_col2:

                if st.button(
                    "🔄",
                    key=f"regen_{index}",
                    help="Regenerate response",
                ):

                    previous_question = None


                    for previous_message in reversed(
                        current_chat.get(
                            "messages",
                            []
                        )[:index]
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


            # ------------------------------------------------
            # POSITIVE FEEDBACK
            # ------------------------------------------------

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


            # ------------------------------------------------
            # NEGATIVE FEEDBACK
            # ------------------------------------------------

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


            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):

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


                        st.markdown(
                            f"**Source {source_number}**"
                        )

                        st.write(
                            page_content
                        )


                        if metadata:

                            st.caption(
                                str(metadata)
                            )

                        if (
                            source_number
                            < len(sources)
                        ):

                            st.markdown("---")


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):

    question = question.strip()

    if not question:
        return


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    add_message(
        current_chat,
        "user",
        question,
    )


    start_time = time.perf_counter()


    try:

        # ----------------------------------------------------
        # GENERATE AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking..."
            ):

                chain = get_qa_chain()

                response = chain(
                    question,
                    chat_history=current_chat[
                        "messages"
                    ][:-1],
                )


            answer = response.get(
                "result",
                "",
            )

            sources = response.get(
                "source_documents",
                [],
            )


            elapsed_time = (
                time.perf_counter()
                - start_time
            )


            # ------------------------------------------------
            # DISPLAY ANSWER
            # ------------------------------------------------

            st.markdown(
                answer
            )


            # ------------------------------------------------
            # DISPLAY SOURCES
            # ------------------------------------------------

            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):

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


                        st.markdown(
                            f"**Source {source_number}**"
                        )

                        st.write(
                            page_content
                        )


                        if metadata:

                            st.caption(
                                str(metadata)
                            )


                        if (
                            source_number
                            < len(sources)
                        ):

                            st.markdown("---")


        # ----------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # ----------------------------------------------------

        add_message(
            current_chat,
            "assistant",
            answer,
            sources=sources,
            response_time=elapsed_time,
        )


    except Exception as error:

        error_message = str(error)

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


# ============================================================
# PENDING SUGGESTED QUESTION
# ============================================================

if st.session_state.pending_question:

    pending_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(
        pending_question
    )

    st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask me anything about our services..."
)


if user_question:

    process_question(
        user_question
    )

    st.rerun()