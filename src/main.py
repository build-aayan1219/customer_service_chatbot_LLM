import os
import sys
import streamlit as st
from dotenv import load_dotenv

# 1. Page Configuration (must be called first so the UI displays immediately)
st.set_page_config(
    page_title="Customer Service AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Environment & Path Setup
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
if KNOWLEDGE_BASE_PATH not in sys.path:
    sys.path.append(KNOWLEDGE_BASE_PATH)

# 3. Custom Styling
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; margin-bottom: 0.75rem; }
    .sentiment-badge {
        display: inline-flex; align-items: center; padding: 3px 10px;
        border-radius: 9999px; font-size: 0.8rem; font-weight: 600; margin-bottom: 8px;
    }
    .sentiment-positive { background-color: rgba(34, 197, 94, 0.15); color: #15803d; border: 1px solid rgba(34, 197, 94, 0.3); }
    .sentiment-negative { background-color: rgba(239, 68, 68, 0.15); color: #b91c1c; border: 1px solid rgba(239, 68, 68, 0.3); }
    .sentiment-neutral  { background-color: rgba(100, 116, 139, 0.15); color: #475569; border: 1px solid rgba(100, 116, 139, 0.3); }
</style>
""", unsafe_allow_html=True)

# 4. Cached / Lazy Model Loading
@st.cache_resource(show_spinner="Loading NLP & Embedding models (this may take a moment on first launch)...")
def load_modules():
    from langchain_helper import get_qa_chain, create_vector_db
    from sentiment_analyzer import analyze_sentiment
    from knowledge_retriever import search_knowledge_base
    return get_qa_chain, create_vector_db, analyze_sentiment, search_knowledge_base

try:
    get_qa_chain, create_vector_db, analyze_sentiment, search_knowledge_base = load_modules()
except Exception as e:
    st.error(f"Error loading models or environment variables: {e}")
    st.info("Make sure your `.env` file has `GOOGLE_API_KEY` set.")
    st.stop()

# 5. Sidebar Controls
with st.sidebar:
    st.title("CustomerAI 🧑‍💻")
    st.caption("Intelligent support powered by dynamic RAG & sentiment analysis")
    st.divider()

    st.subheader("Knowledge Base")
    if st.button("🔄 Rebuild Knowledge Base", use_container_width=True):
        with st.spinner("Indexing documents and building vector store..."):
            create_vector_db()
        st.success("Knowledge base index created successfully!")

    st.divider()
    st.subheader("Retrieval Settings")
    top_k_val = st.slider("Dynamic KB Top Matches", min_value=1, max_value=5, value=3)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Header
st.title("Customer Service Chatbot")
st.caption("Ask questions about policies, courses, or technical details.")

# 8. Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            sentiment = msg.get("sentiment", "Neutral")
            badge_class = f"sentiment-{sentiment.lower()}"
            st.markdown(
                f'<span class="sentiment-badge {badge_class}">Detected Sentiment: {sentiment}</span>',
                unsafe_allow_html=True
            )
            st.write(msg["content"])
            if msg.get("kb_result"):
                kb = msg["kb_result"]
                with st.expander("🔍 Knowledge Base Retrieval Details"):
                    st.markdown(f"**Retrieved Content:**\n\n>{kb['content']}")
                    cols = st.columns(3)
                    cols[0].metric("Source", kb.get("source", "N/A"))
                    cols[1].metric("Relevance Score", f"{kb.get('score', 0):.4f}" if isinstance(kb.get('score'), float) else str(kb.get('score')))
                    cols[2].metric("Last Updated", kb.get("updated_at", "N/A"))
        else:
            st.write(msg["content"])

# 9. Handle User Question
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing sentiment and retrieving answer..."):
            sentiment, scores = analyze_sentiment(prompt)
            kb_results = search_knowledge_base(prompt, top_k=top_k_val)
            best_kb = kb_results[0] if kb_results else None

            if sentiment == "Negative":
                prefix = "I'm sorry that you're experiencing an issue. Here's the information that may help:\n\n"
            elif sentiment == "Positive":
                prefix = "Thank you for your positive message! Here's the information you requested:\n\n"
            else:
                prefix = "Here's the information related to your question:\n\n"

            chain = get_qa_chain()
            response = chain(prompt)
            answer_text = prefix + response.get("result", "")

            badge_class = f"sentiment-{sentiment.lower()}"
            st.markdown(
                f'<span class="sentiment-badge {badge_class}">Detected Sentiment: {sentiment}</span>',
                unsafe_allow_html=True
            )
            st.write(answer_text)

            if best_kb:
                with st.expander("🔍 Knowledge Base Retrieval Details"):
                    st.markdown(f"**Retrieved Content:**\n\n>{best_kb['content']}")
                    cols = st.columns(3)
                    cols[0].metric("Source", best_kb.get("source", "N/A"))
                    cols[1].metric("Relevance Score", f"{best_kb.get('score', 0):.4f}" if isinstance(best_kb.get('score'), float) else str(best_kb.get('score')))
                    cols[2].metric("Last Updated", best_kb.get("updated_at", "N/A"))

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer_text,
                "sentiment": sentiment,
                "kb_result": best_kb
            })
