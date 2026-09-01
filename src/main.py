import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Customer Service Assistant",
    page_icon="🤖",
    layout="centered"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
    max-width: 900px;
}

/* Header */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Welcome section */
.welcome {
    text-align: center;
    padding: 30px 20px;
    margin-bottom: 10px;
}

.welcome-icon {
    font-size: 55px;
}

.welcome-title {
    font-size: 25px;
    font-weight: 600;
    margin-top: 10px;
}

.welcome-text {
    color: #9ca3af;
    font-size: 15px;
    margin-top: 8px;
}

/* Suggestion buttons */
div.stButton > button {
    border-radius: 10px;
    min-height: 45px;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    font-size: 13px;
    margin-top: 20px;
    padding-bottom: 10px;
}

/* Source information */
.source-title {
    font-weight: 600;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- SOURCE DISPLAY ----------------

def display_sources(sources):

    if not sources:
        return

    with st.expander("📚 View Source Information"):

        st.caption(
            "Information retrieved from the FAQ knowledge base."
        )

        for i, document in enumerate(sources, 1):

            st.markdown(f"### 📄 Source {i}")

            content = document.page_content

            question_text = ""
            answer_text = ""

            if "prompt:" in content.lower() and "response:" in content.lower():

                parts = content.split("response:", 1)

                question_text = parts[0].replace(
                    "prompt:", ""
                ).strip()

                answer_text = parts[1].strip()

            else:

                answer_text = content

            if question_text:

                st.markdown("**Question**")
                st.write(question_text)

            st.markdown("**Answer**")
            st.write(answer_text)

            if i < len(sources):
                st.divider()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.subheader("📚 Knowledge Base")

    st.caption(
        "FAQ knowledge base used by the chatbot."
    )

    if st.button(
        "🔄 Create / Update Knowledge Base",
        use_container_width=True
    ):

        with st.spinner("Updating knowledge base..."):

            try:

                create_vector_db()

                st.success(
                    "Knowledge base updated successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    st.success("🟢 Knowledge Base Ready")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.subheader("ℹ️ About")

    st.write(
        "An AI-powered customer service chatbot that "
        "uses Retrieval-Augmented Generation (RAG) "
        "to answer questions from a trusted FAQ "
        "knowledge base."
    )

    st.divider()

    st.caption("Technology Stack")

    st.write(
        "🤖 Gemini\n\n"
        "🔎 FAISS\n\n"
        "🧠 Hugging Face Embeddings\n\n"
        "🌐 Streamlit"
    )


# ---------------- HEADER ----------------

st.markdown(
    '<div class="title">🤖 AI Customer Service Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions and get reliable answers from our knowledge base.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- WELCOME SCREEN ----------------

# ---------------- WELCOME SCREEN ----------------

if not st.session_state.messages:

    st.markdown(
        """
<div class="welcome">
    <div class="welcome-icon">💬</div>
    <div class="welcome-title">How can I help you?</div>
    <div class="welcome-text">
        Ask me about courses, internships, services,
        tools and other available information.
    </div>
</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    # ---------------- SUGGESTION 1 ----------------

    with col1:

        if st.button(
            "🎓 Do you provide internships?",
            use_container_width=True
        ):

            question = "Do you provide internships?"

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            try:
                chain = get_qa_chain()
                response = chain(question)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["result"],
                    "sources": response.get("source_documents", [])
                })

            except Exception:

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I couldn't process your question.",
                    "sources": []
                })

            st.rerun()

    # ---------------- SUGGESTION 2 ----------------

    with col2:

        if st.button(
            "💳 Do you offer EMI?",
            use_container_width=True
        ):

            question = "Do you offer EMI?"

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            try:
                chain = get_qa_chain()
                response = chain(question)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["result"],
                    "sources": response.get("source_documents", [])
                })

            except Exception:

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I couldn't process your question.",
                    "sources": []
                })

            st.rerun()

    col3, col4 = st.columns(2)

    # ---------------- SUGGESTION 3 ----------------

    with col3:

        if st.button(
            "💻 Can I use Power BI on Mac?",
            use_container_width=True
        ):

            question = "Can I use Power BI on Mac?"

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            try:
                chain = get_qa_chain()
                response = chain(question)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["result"],
                    "sources": response.get("source_documents", [])
                })

            except Exception:

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I couldn't process your question.",
                    "sources": []
                })

            st.rerun()

    # ---------------- SUGGESTION 4 ----------------

    with col4:

        if st.button(
            "📊 Tableau vs Power BI?",
            use_container_width=True
        ):

            question = "Which is better, Tableau or Power BI?"

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            try:
                chain = get_qa_chain()
                response = chain(question)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["result"],
                    "sources": response.get("source_documents", [])
                })

            except Exception:

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I couldn't process your question.",
                    "sources": []
                })

            st.rerun()


# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            display_sources(
                message.get("sources", [])
            )


# ---------------- CHAT INPUT ----------------

question = st.chat_input(
    "Ask your question..."
)


if question:

    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                chain = get_qa_chain()

                response = chain(question)

                answer = response["result"]

                sources = response.get(
                    "source_documents",
                    []
                )

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

                display_sources(sources)

            except Exception:

                error_message = (
                    "Sorry, I couldn't process your question."
                )

                st.error(error_message)

                st.caption(
                    "Please try again."
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                })


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    '<div class="footer">'
    'Powered by Gemini • FAISS • Hugging Face • Streamlit'
    '</div>',
    unsafe_allow_html=True
)