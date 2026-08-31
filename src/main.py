import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Customer Service Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 16px;
    margin-bottom: 30px;
}

.chat-user {
    background-color: #e8f0fe;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 10px 0;
}

.chat-bot {
    background-color: #f1f3f4;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🤖 Customer Service Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions and get instant answers from our knowledge base.</div>',
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    st.write("### Knowledge Base")

    if st.button("📚 Create Knowledge Base", use_container_width=True):

        with st.spinner("Creating knowledge base..."):
            try:
                create_vector_db()
                st.success("Knowledge base created successfully!")

            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()

    st.write("### About")
    st.write(
        "This chatbot uses Generative AI, "
        "LangChain and FAISS to answer questions "
        "from the provided FAQ dataset."
    )


# ---------------- CHAT INPUT ----------------
question = st.chat_input("💬 Ask your question...")


# ---------------- ANSWER ----------------
if question:

    # Display user question
    with st.chat_message("user"):
        st.write(question)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                chain = get_qa_chain()
                response = chain(question)

                answer = response["result"]

                st.write(answer)

            except Exception as e:
                st.error(f"Unable to generate answer: {e}")


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "Powered by Google Gemini • LangChain • FAISS • Streamlit"
)