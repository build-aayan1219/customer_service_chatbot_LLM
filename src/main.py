import streamlit as st
import os

from langchain_helper import create_vector_db, get_answer


st.set_page_config(
    page_title="Customer Service Chatbot",
    page_icon="🤖"
)

# CSS
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.answer {
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


# Title
st.markdown(
    '<div class="title">🤖 Customer Service Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about our courses and services.</div>',
    unsafe_allow_html=True
)


# Knowledge Base
st.subheader("📚 Knowledge Base")

if st.button("🔄 Create Knowledge Base"):

    with st.spinner("Creating Knowledge Base..."):

        try:
            create_vector_db()
            st.success("Knowledge Base created successfully! ✅")

        except Exception as e:
            st.error(f"Error: {e}")


st.divider()


# Question
st.subheader("💬 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: Do you provide virtual internships?"
)


# Answer
if question:

    if not os.path.exists("faiss_index"):

        st.warning("Please create the Knowledge Base first.")

    else:

        with st.spinner("Finding the best answer..."):

            try:
                answer = get_answer(question)

                st.subheader("📝 Answer")

                st.markdown(
                    f'<div class="answer">{answer}</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Error while getting answer: {e}")


st.divider()

st.caption(
    "Powered by Gemini • LangChain • FAISS • Hugging Face"
)