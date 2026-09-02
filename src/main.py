import streamlit as st
import logging
from langchain_helper import get_qa_chain, create_vector_db

# Set up logging
logger = logging.getLogger(__name__)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Customer Service Assistant",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .welcome {
        text-align: center;
        padding: 2rem;
        margin-bottom: 1.5rem;
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
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sources" not in st.session_state:
    st.session_state.sources = []


# --------------------------------------------------
# HELPER FUNCTION - PROCESS QUESTION
# --------------------------------------------------

def process_question(question_text: str):
    """
    Process any question and handle all logic.
    Used for both suggested questions and chat input.
    """
    
    logger.info(f"Processing question: {question_text[:50]}...")
    
    st.session_state.messages.append({
        "role": "user",
        "content": question_text
    })
    
    try:
        with st.spinner("Thinking..."):
            chain = get_qa_chain()
            response = chain(question_text)
        
        answer = response["result"]
        sources = response.get("source_documents", [])
        
        logger.info(f"Got answer with {len(sources)} sources")
        
        st.markdown(answer)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
        
        st.session_state.sources.append(sources)
        
        # Show sources
        if sources:
            with st.expander("📚 View Source Information"):
                for source in sources:
                    content = source.page_content
                    lines = content.split("\n")
                    
                    question = ""
                    answer_text = ""
                    
                    for line in lines:
                        if line.lower().startswith("prompt:"):
                            question = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("response:"):
                            answer_text = line.split(":", 1)[1].strip()
                    
                    if question:
                        st.markdown(f"**Question:** {question}")
                    if answer_text:
                        st.markdown(f"**Answer:** {answer_text}")
                    st.markdown("---")
        
        st.rerun()
    
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error processing question: {error_message}", exc_info=True)
        
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            st.warning(
                "⚠️ **AI service temporarily unavailable**\n\n"
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )
        else:
            st.error(
                "❌ **Unable to process your question**\n\n"
                "Please try again."
            )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("### Knowledge Base")

    if st.button("🔄 Create / Update Knowledge Base", use_container_width=True):

        logger.info("User clicked: Create Knowledge Base")

        try:
            with st.spinner("Updating knowledge base..."):
                create_vector_db()

            logger.info("✓ Knowledge base created successfully")
            st.success("Knowledge base updated successfully!")

        except Exception as e:
            error_message = str(e)
            logger.error(f"Error creating KB: {error_message}", exc_info=True)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.warning(
                    "⚠️ Gemini API usage limit has been reached. "
                    "The knowledge base itself may still be updated."
                )
            else:
                st.error("❌ Could not update the knowledge base.")

    st.markdown("")

    st.success("🟢 Knowledge Base Ready")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources = []
        st.rerun()

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


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🤖 AI Customer Service Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions and get answers from our knowledge base</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

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


# --------------------------------------------------
# SUGGESTED QUESTIONS
# --------------------------------------------------

st.markdown("### 💡 Try asking")

questions = [
    {"emoji": "🎓", "text": "Do you provide internships?", "col": 0},
    {"emoji": "💳", "text": "Do you offer EMI?", "col": 1},
    {"emoji": "💻", "text": "Can I use Power BI on Mac?", "col": 0},
    {"emoji": "📊", "text": "Tableau vs Power BI?", "col": 1},
]

col1, col2 = st.columns(2)
cols = [col1, col2]

for q in questions:
    with cols[q["col"]]:
        if st.button(f"{q['emoji']} {q['text']}", use_container_width=True):
            logger.info(f"User clicked suggested question: {q['text']}")
            process_question(q["text"])


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if index // 2 < len(st.session_state.sources):

                sources = st.session_state.sources[index // 2]

                if sources:

                    with st.expander("📚 View Source Information"):

                        for source in sources:

                            content = source.page_content

                            lines = content.split("\n")

                            question = ""
                            answer = ""

                            for line in lines:

                                if line.lower().startswith("prompt:"):
                                    question = line.split(
                                        ":", 1
                                    )[1].strip()

                                elif line.lower().startswith("response:"):
                                    answer = line.split(
                                        ":", 1
                                    )[1].strip()

                            if question:
                                st.markdown(
                                    f"**Question:** {question}"
                                )

                            if answer:
                                st.markdown(
                                    f"**Answer:** {answer}"
                                )

                            st.markdown("---")


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_question = st.chat_input("Ask me anything about our services...")

if user_question:

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        process_question(user_question)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Built with Python, Streamlit, LangChain, Gemini, HuggingFace & FAISS
    </div>
    """,
    unsafe_allow_html=True
)