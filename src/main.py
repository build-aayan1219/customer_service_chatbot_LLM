import sys
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ==================================================
# PATH SETUP
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ==================================================
# SESSION STATE
# ==================================================

if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False

if "show_knowledge_base" not in st.session_state:
    st.session_state.show_knowledge_base = False


# ==================================================
# IMPORTS
# ==================================================

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

from src.knowledge_base import (
    render_knowledge_base,
)

from src.langchain_helper import (
    create_vector_db,
    get_qa_chain,
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
# MAIN CSS
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

    .welcome-heading {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .welcome-description {
        color: #777;
        font-size: 15px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# LOAD CHATS
# ==================================================

if "chats" not in st.session_state:

    st.session_state.chats = load_chats()


# ==================================================
# CURRENT CHAT
# ==================================================

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


# ==================================================
# SEARCH
# ==================================================

if "search_text" not in st.session_state:

    st.session_state.search_text = ""


# ==================================================
# FIND CURRENT CHAT
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


# ==================================================
# ANALYTICS / KNOWLEDGE BASE VIEW
# ==================================================

if (
    st.session_state.show_analytics
    or st.session_state.show_knowledge_base
):

    with st.sidebar:

        st.markdown(
            "## 🤖 AI Customer Support"
        )

        st.markdown("---")


        # ----------------------------------------------
        # BACK TO CHAT
        # ----------------------------------------------

        if st.button(
            "← Back to Chat",
            use_container_width=True,
        ):

            st.session_state.show_analytics = False

            st.session_state.show_knowledge_base = False

            st.rerun()


        st.markdown("---")


        # ----------------------------------------------
        # ANALYTICS
        # ----------------------------------------------

        if st.button(
            "📊 Analytics",
            use_container_width=True,
        ):

            st.session_state.show_analytics = True

            st.session_state.show_knowledge_base = False

            st.rerun()


        # ----------------------------------------------
        # KNOWLEDGE BASE
        # ----------------------------------------------

        if st.button(
            "📚 Knowledge Base",
            use_container_width=True,
        ):

            st.session_state.show_analytics = False

            st.session_state.show_knowledge_base = True

            st.rerun()


        st.markdown("---")


        if st.session_state.show_analytics:

            st.success(
                "Analytics Active"
            )

        else:

            st.success(
                "Knowledge Base Active"
            )


    if st.session_state.show_analytics:

        render_analytics()

    elif st.session_state.show_knowledge_base:

        render_knowledge_base()

    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        "## 🤖 AI Customer Support"
    )

    st.markdown("")


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

        st.rerun()


    st.markdown("---")


    # ----------------------------------------------
    # ANALYTICS
    # ----------------------------------------------

    st.markdown(
        "### 📊 Dashboard"
    )


    if st.button(
        "📊 Analytics",
        use_container_width=True,
    ):

        st.session_state.show_analytics = True

        st.session_state.show_knowledge_base = False

        st.rerun()


    # ----------------------------------------------
    # KNOWLEDGE BASE
    # ----------------------------------------------

    if st.button(
        "📚 Knowledge Base",
        use_container_width=True,
    ):

        st.session_state.show_analytics = False

        st.session_state.show_knowledge_base = True

        st.rerun()


    st.markdown("---")


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


    st.markdown("---")


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

                st.rerun()


    st.markdown("---")


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

        st.session_state.chats = (
            delete_chat(
                st.session_state.chats,
                current_chat["id"],
            )
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


    # ----------------------------------------------
    # QUICK KNOWLEDGE BASE UPDATE
    # ----------------------------------------------

    st.markdown(
        "### 📚 Quick Knowledge Base Update"
    )


    if st.button(
        "🔄 Rebuild Knowledge Base",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Updating knowledge base..."
            ):

                create_vector_db()


            st.success(
                "Knowledge base updated."
            )


        except Exception as error:

            error_message = str(
                error
            )


            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED"
                in error_message
            ):

                st.warning(
                    "Gemini API usage limit "
                    "has been reached."
                )

            else:

                st.error(
                    "Could not update the "
                    "knowledge base."
                )


    st.success(
        "🟢 Knowledge Base Ready"
    )


    st.markdown("---")


    # ----------------------------------------------
    # ABOUT
    # ----------------------------------------------

    st.markdown(
        "### ℹ️ About"
    )


    st.write(
        """
        This AI Customer Support Assistant uses
        Retrieval-Augmented Generation (RAG)
        to answer questions using information
        from the available knowledge base.
        """
    )


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
# HEADER
# ==================================================

st.markdown(
    '<div class="title">'
    '🤖 AI Customer Service Assistant'
    '</div>',
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="subtitle">'
    'Ask questions and get answers from our knowledge base'
    '</div>',
    unsafe_allow_html=True,
)


# ==================================================
# WELCOME
# ==================================================

if not current_chat["messages"]:

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-icon">
                💬
            </div>

            <div class="welcome-heading">
                How can I help you?
            </div>

            <div class="welcome-description">
                Ask me about courses, internships,
                services, tools and other available
                information.
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
# DISPLAY CHAT
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


    with st.chat_message(
        role
    ):

        st.markdown(
            content
        )


        if role == "assistant":

            sources = message.get(
                "sources",
                [],
            )


            button_col1, button_col2, button_col3, button_col4 = st.columns(
                [1, 1, 1, 1]
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
                        current_chat["messages"][
                            :index
                        ]
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
            # POSITIVE FEEDBACK
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
            # NEGATIVE FEEDBACK
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
                                str(
                                    metadata
                                )
                            )


                        st.markdown(
                            "---"
                        )


# ==================================================
# PROCESS QUESTION
# ==================================================

def process_question(
    question
):

    question = question.strip()


    if not question:
        return


    add_message(
        current_chat,
        "user",
        question,
    )


    start_time = (
        time.perf_counter()
    )


    try:

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                chain = get_qa_chain()


                response = chain(
                    question,
                    chat_history=(
                        current_chat[
                            "messages"
                        ][:-1]
                    ),
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


            st.markdown(
                answer
            )


            if sources:

                with st.expander(
                    "📚 View Sources"
                ):

                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):

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
                                str(
                                    metadata
                                )
                            )


                        st.markdown(
                            "---"
                        )


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
            "pending_question"
        )
    )


    process_question(
        pending_question
    )


    st.rerun()


# ==================================================
# CHAT INPUT
# ==================================================

user_question = st.chat_input(
    "Ask me anything about our services..."
)


if user_question:

    process_question(
        user_question
    )


    st.rerun()