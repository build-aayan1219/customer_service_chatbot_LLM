import os
import re
import sys
import streamlit as st
from dotenv import load_dotenv

# 1. Ensure Python can find all project folders (fixes 'No module named src')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
KNOWLEDGE_BASE_DIR = os.path.join(PROJECT_ROOT, "knowledge_base")

for p in [CURRENT_DIR, PROJECT_ROOT, KNOWLEDGE_BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# 2. Page Configuration (displays instantly)
st.set_page_config(
    page_title="Customer Service Chatbot",
    page_icon="🤖",
    layout="wide"
)

# 3. Load .env file
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# 4. Safe imports (works with both 'src.' and direct imports)
from langchain_helper import (
    create_vector_db,
    get_qa_chain,
    retrieve_documents,
)


def analyze_sentiment(text):
    """Return the sentiment contract expected by the chat UI."""
    positive_words = {
        "amazing", "awesome", "excellent", "good", "great", "happy",
        "helpful", "love", "perfect", "thanks", "thank", "wonderful",
    }
    negative_words = {
        "angry", "bad", "broken", "disappointed", "error", "hate",
        "issue", "poor", "problem", "refund", "sad", "terrible",
    }
    words = set(re.findall(r"\b[a-z]+\b", str(text).lower()))
    positive_score = len(words & positive_words)
    negative_score = len(words & negative_words)

    if negative_score > positive_score:
        sentiment = "Negative"
    elif positive_score > negative_score:
        sentiment = "Positive"
    else:
        sentiment = "Neutral"

    return sentiment, {
        "Positive": positive_score,
        "Negative": negative_score,
        "Neutral": int(sentiment == "Neutral"),
    }


def search_knowledge_base(query, top_k=3):
    """Adapt the shared document retriever to the UI's source format."""
    results = []
    for document in retrieve_documents(query):
        metadata = getattr(document, "metadata", {}) or {}
        results.append({
            "content": getattr(document, "page_content", ""),
            "source": metadata.get("source_file") or metadata.get("source") or "Unknown",
            "score": metadata.get("relevance_score", 0.0),
        })
        if len(results) >= top_k:
            break
    return results


# 5. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Knowledge Base")
    st.write("Manage your local vector store:")
    if st.button("Create / Rebuild Knowledgebase", use_container_width=True):
        with st.spinner("Building vector database..."):
            try:
                create_vector_db()
                st.success("Knowledgebase created successfully!")
            except Exception as e:
                st.error(f"Failed to create database: {e}")

    st.divider()
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# 6. Main Chat Header
st.title("CUSTOMER SERVICE CHATBOT 🤖")
st.caption("Ask questions about products, courses, or services.")

# 7. Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 8. Render conversation history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sentiment"):
            st.caption(f"**Detected Sentiment:** {msg['sentiment']}")
        if msg.get("kb_result"):
            kb = msg["kb_result"]
            with st.expander("📚 Retrieved Knowledge Source"):
                st.markdown(f"**Content:** {kb['content']}")
                st.markdown(f"**Source:** {kb['source']} | **Relevance:** {kb['score']}")

# 9. User Input Box
user_prompt = st.chat_input("Type your question here...")

if user_prompt:
    # 1. Add user message to UI
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Task 1: Sentiment Analysis
            sentiment, scores = analyze_sentiment(user_prompt)

            # Task 3: Dynamic Knowledge Base Retrieval
            kb_results = search_knowledge_base(user_prompt, top_k=3)
            best_kb = kb_results[0] if kb_results else None

            # Sentiment-aware prefix
            if sentiment == "Negative":
                prefix = "I'm sorry that you're experiencing an issue. Here's the information that may help:\n\n"
            elif sentiment == "Positive":
                prefix = "Thank you for your positive message! Here's the information you requested:\n\n"
            else:
                prefix = "Here's the information related to your question:\n\n"

            # Task 2: QA Chain Answer (loaded on demand)
            try:
                chain = get_qa_chain()
                response = chain(user_prompt)
                answer_text = prefix + response.get("result", "")
            except Exception as e:
                answer_text = prefix + f"Could not retrieve answer from QA chain: {e}"

            # Display response
            st.markdown(answer_text)
            st.caption(f"**Detected Sentiment:** {sentiment}")

            if best_kb:
                with st.expander("📚 Retrieved Knowledge Source"):
                    st.markdown(f"**Content:** {best_kb['content']}")
                    st.markdown(f"**Source:** {best_kb['source']} | **Relevance:** {best_kb['score']}")

            # Save assistant message in history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer_text,
                "sentiment": sentiment,
                "kb_result": best_kb
            })
