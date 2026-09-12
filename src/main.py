import base64
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.chat_manager import (
    add_message,
    create_chat,
    delete_all_chats,
    delete_chat,
    find_chat,
    load_chats,
    remove_message,
    rename_chat,
    search_chats,
    set_chat_archived,
    set_chat_pinned,
    truncate_chat,
    update_message_feedback,
)
from src.langchain_helper import get_qa_stream
from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    delete_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)
from src.config import LLM_CONFIG, SUGGESTED_QUESTIONS

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container {padding-top:1.15rem; padding-bottom:7rem; max-width:1180px;}
section[data-testid="stSidebar"] {min-width:300px; max-width:340px;}
section[data-testid="stSidebar"] .stButton > button {white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.title {font-size:2rem;font-weight:750;letter-spacing:-.03em;margin:0;}
.subtitle {color:#777;margin-top:2px;margin-bottom:18px;}
.welcome {max-width:760px;margin:70px auto 24px;padding:44px 28px;text-align:center;border:1px solid rgba(128,128,128,.18);border-radius:24px;background:rgba(128,128,128,.045);}
.welcome-icon {font-size:42px}.welcome-title {font-size:28px;font-weight:750;margin:10px 0}.welcome-text{color:#777;line-height:1.6}
.source-group {border:1px solid rgba(128,128,128,.20);border-radius:14px;padding:13px 15px;margin:8px 0;background:rgba(128,128,128,.035);}
.source-file {font-weight:700}.source-meta{font-size:12px;color:#777;margin-top:3px}.source-section{font-size:13px;margin-top:9px;padding-top:8px;border-top:1px solid rgba(128,128,128,.13)}
.file-card {border:1px solid rgba(128,128,128,.18);border-radius:13px;padding:12px;margin:6px 0;background:rgba(128,128,128,.035);}
.small-muted {font-size:12px;color:#777;}
.stat-card {padding:18px;border:1px solid rgba(128,128,128,.18);border-radius:16px;background:rgba(128,128,128,.04);}
.sidebar-brand {font-size:19px;font-weight:750;margin-bottom:12px;}
.chat-context {padding:9px 13px;border:1px solid rgba(128,128,128,.16);border-radius:12px;background:rgba(128,128,128,.035);margin:0 0 14px;}
.chat-context strong {font-size:13px;}
.chat-context span {font-size:12px;color:#777;}
</style>
""",
    unsafe_allow_html=True,
)


def init_state():
    if "chats" not in st.session_state:
        st.session_state.chats = load_chats()
    if not st.session_state.chats:
        first = create_chat()
        st.session_state.chats = [first]
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = st.session_state.chats[0]["id"]
    if "search_text" not in st.session_state:
        st.session_state.search_text = ""
    if "show_archived" not in st.session_state:
        st.session_state.show_archived = False
    if "show_dashboard" not in st.session_state:
        st.session_state.show_dashboard = False
    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None
    if "pending_regenerate" not in st.session_state:
        st.session_state.pending_regenerate = None
    if "temperature" not in st.session_state:
        st.session_state.temperature = float(LLM_CONFIG.get("temperature", 0.1))


init_state()
current_chat = find_chat(st.session_state.chats, st.session_state.current_chat_id)
if current_chat is None:
    current_chat = create_chat()
    st.session_state.chats.insert(0, current_chat)
    st.session_state.current_chat_id = current_chat["id"]
current_chat_id = current_chat["id"]


def refresh_chats():
    st.session_state.chats = load_chats()


def clean_source(source):
    if isinstance(source, dict):
        return str(source.get("page_content", "") or "").strip(), source.get("metadata", {}) or {}
    return str(getattr(source, "page_content", "") or "").strip(), getattr(source, "metadata", {}) or {}


def source_group_key(metadata):
    source_type = metadata.get("source_type", "global_knowledge")
    if source_type == "conversation_file":
        name = metadata.get("source_file") or metadata.get("file_name") or metadata.get("filename") or "Conversation file"
        return ("file", Path(str(name)).name)
    return ("global", "Knowledge Base")


def render_sources(sources):
    if not sources:
        return
    groups = defaultdict(list)
    for source in sources:
        content, metadata = clean_source(source)
        if not isinstance(metadata, dict):
            metadata = {}
        groups[source_group_key(metadata)].append((content, metadata))

    with st.expander(f"📚 Sources · {len(groups)} source{'s' if len(groups) != 1 else ''}"):
        for (kind, name), items in groups.items():
            icon = "📄" if kind == "file" else "📚"
            section_label = "section" if len(items) == 1 else "sections"
            source_label = "Conversation file" if kind == "file" else "Knowledge Base"
            st.markdown(
                f'<div class="source-group"><div class="source-file">{icon} {name}</div>'
                f'<div class="source-meta">{len(items)} relevant {section_label} · {source_label}</div></div>',
                unsafe_allow_html=True,
            )
            for number, (content, metadata) in enumerate(items, start=1):
                section = metadata.get("section") or metadata.get("location") or "Relevant section"
                with st.expander(f"{section}", expanded=False):
                    st.write(content)
                    extra = []
                    if metadata.get("location") and metadata.get("location") != section:
                        extra.append(str(metadata["location"]))
                    if metadata.get("chunk_index") is not None:
                        extra.append(f"chunk {metadata['chunk_index']}")
                    if extra:
                        st.caption(" · ".join(extra))


def copy_button(text, key):
    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    components.html(
        f"""
        <script>
        const text = atob('{encoded}');
        const b = document.createElement('button');
        b.innerText = 'Copy';
        b.style.cssText = 'padding:4px 10px;border:1px solid #888;border-radius:8px;background:transparent;cursor:pointer;font-size:12px;';
        b.onclick = async () => {{ await navigator.clipboard.writeText(text); b.innerText='Copied'; setTimeout(()=>b.innerText='Copy',1200); }};
        document.body.appendChild(b);
        </script>
        """,
        height=32,
        key=key,
    )


def export_markdown(chat):
    lines = [f"# {chat.get('title', 'Conversation')}", "", f"Created: {chat.get('created_at', '')}", ""]
    for message in chat.get("messages", []):
        role = "You" if message.get("role") == "user" else "AI Customer Support"
        lines.extend([f"## {role}", "", message.get("content", ""), ""])
        sources = message.get("sources", [])
        if sources:
            lines.append("### Sources")
            seen = set()
            for source in sources:
                _, metadata = clean_source(source)
                name = metadata.get("source_file") or metadata.get("file_name") or metadata.get("filename") or "Knowledge Base"
                name = Path(str(name)).name if name != "Knowledge Base" else name
                section = metadata.get("section") or metadata.get("location") or "Relevant section"
                key = (name, section)
                if key not in seen:
                    lines.append(f"- {name} — {section}")
                    seen.add(key)
            lines.append("")
    return "\n".join(lines)


def new_chat():
    chat = create_chat()
    st.session_state.chats.insert(0, chat)
    st.session_state.current_chat_id = chat["id"]
    st.session_state.show_dashboard = False
    st.rerun()


def handle_delete_chat():
    chat_id = current_chat_id
    st.session_state.chats = delete_chat(st.session_state.chats, chat_id)
    delete_conversation_files(chat_id)
    if not st.session_state.chats:
        replacement = create_chat()
        st.session_state.chats = [replacement]
    st.session_state.current_chat_id = st.session_state.chats[0]["id"]
    st.session_state.editing_index = None
    st.rerun()


def dashboard():
    chats = st.session_state.chats
    questions = []
    responses = []
    response_times = []
    positive = negative = 0
    for chat in chats:
        for message in chat.get("messages", []):
            if message.get("role") == "user":
                questions.append(message.get("content", ""))
            elif message.get("role") == "assistant":
                responses.append(message.get("content", ""))
                if isinstance(message.get("response_time"), (int, float)):
                    response_times.append(message["response_time"])
                if message.get("feedback") == "positive":
                    positive += 1
                elif message.get("feedback") == "negative":
                    negative += 1
    unknown = sum("I don't know based on the available information." in r for r in responses)
    avg_time = sum(response_times) / len(response_times) if response_times else 0
    feedback_total = positive + negative
    satisfaction = (positive / feedback_total * 100) if feedback_total else 0

    st.markdown("# 📊 Dashboard")
    st.caption("Product usage and assistant performance across saved conversations.")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Conversations", len(chats))
    c2.metric("Questions", len(questions))
    c3.metric("Responses", len(responses))
    c4.metric("Avg response", f"{avg_time:.2f}s")
    c5.metric("Satisfaction", f"{satisfaction:.0f}%")

    st.markdown("### Performance")
    p1, p2, p3 = st.columns(3)
    p1.metric("Unknown responses", unknown)
    p2.metric("Positive feedback", positive)
    p3.metric("Negative feedback", negative)

    st.markdown("### Recent conversations")
    if chats:
        rows = []
        for chat in chats[:15]:
            rows.append({
                "Conversation": chat.get("title", "New Chat"),
                "Messages": len(chat.get("messages", [])),
                "Pinned": "Yes" if chat.get("pinned") else "No",
                "Updated": chat.get("updated_at", ""),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No conversation data yet.")

    if st.button("← Back to chat", use_container_width=False):
        st.session_state.show_dashboard = False
        st.rerun()


# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🤖 AI Customer Support</div>', unsafe_allow_html=True)
    if st.button("＋ New Chat", use_container_width=True, type="primary"):
        new_chat()

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()

    st.markdown("---")
    search = st.text_input("Search conversations", value=st.session_state.search_text, placeholder="Search chats...", label_visibility="collapsed")
    st.session_state.search_text = search

    st.markdown("### Conversations")
    visible = [c for c in search_chats(st.session_state.chats, search) if st.session_state.show_archived or not c.get("archived", False)]
    pinned = [c for c in visible if c.get("pinned")]
    regular = [c for c in visible if not c.get("pinned")]

    if pinned:
        st.caption("PINNED")
        for chat in pinned:
            label = ("🟢 " if chat["id"] == current_chat_id else "📌 ") + chat.get("title", "New Chat")
            if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.show_dashboard = False
                st.rerun()

    if regular:
        for chat in regular:
            label = ("🟢 " if chat["id"] == current_chat_id else "💬 ") + chat.get("title", "New Chat")
            if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.show_dashboard = False
                st.rerun()

    if not visible:
        st.caption("No matching conversations.")

    st.checkbox("Show archived", key="show_archived")
    st.markdown("---")

    with st.expander("⚙️ Response settings"):
        st.caption(f"Model: `{LLM_CONFIG.get('model', 'Gemini')}`")
        st.slider("Creativity", 0.0, 1.0, key="temperature", step=0.05, help="Lower values are more focused; higher values are more creative.")
        st.caption("Retrieval and knowledge-source behavior remain controlled by the application configuration.")

    with st.expander("ℹ️ About"):
        st.write("A RAG-powered AI customer support and document assistant using Gemini, LangChain, FAISS and conversation-scoped files.")
        st.caption("Python · Streamlit · LangChain · Gemini · HuggingFace · FAISS · SQLite")

if st.session_state.show_dashboard:
    dashboard()
    st.stop()

# Header
header_col, action_col = st.columns([8, 1])
with header_col:
    st.markdown(f'<div class="title">🤖 {current_chat.get("title", "New Chat")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ask questions, attach documents, and work with your conversation context.</div>', unsafe_allow_html=True)
with action_col:
    with st.popover("⋯"):
        new_title = st.text_input("Conversation name", value=current_chat.get("title", "New Chat"), key="header_rename")
        if st.button("Rename", use_container_width=True):
            rename_chat(current_chat, new_title)
            refresh_chats()
            st.rerun()
        if current_chat.get("pinned"):
            if st.button("Unpin", use_container_width=True):
                set_chat_pinned(current_chat, False)
                refresh_chats(); st.rerun()
        else:
            if st.button("Pin", use_container_width=True):
                set_chat_pinned(current_chat, True)
                refresh_chats(); st.rerun()
        if current_chat.get("archived"):
            if st.button("Unarchive", use_container_width=True):
                set_chat_archived(current_chat, False)
                refresh_chats(); st.rerun()
        else:
            if st.button("Archive", use_container_width=True):
                set_chat_archived(current_chat, True)
                refresh_chats(); st.rerun()
        st.download_button("Export Markdown", export_markdown(current_chat), file_name=f"{current_chat.get('title','conversation').replace(' ','_')}.md", mime="text/markdown", use_container_width=True)
        if st.button("Delete conversation", use_container_width=True):
            handle_delete_chat()

# Attachments
files = list_conversation_files(current_chat_id)
if files:
    with st.expander(f"📎 Attached files · {len(files)}", expanded=False):
        for record in files:
            file_id = record.get("id")
            name = record.get("file_name", "Attached file")
            size = record.get("size", 0)
            chunks = record.get("chunk_count", 0)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**📄 {name}**")
                st.caption(f"{size / 1024:.1f} KB · {chunks} chunks")
            with col2:
                if st.button("Remove", key=f"remove_file_{file_id}"):
                    remove_conversation_file(current_chat_id, file_id)
                    st.rerun()

if files:
    st.markdown(
        f'<div class="chat-context"><strong>📎 {len(files)} file{'s' if len(files) != 1 else ""} attached</strong><br><span>Ask about the files directly — for example: “What is the code related to?”</span></div>',
        unsafe_allow_html=True,
    )

if not current_chat["messages"]:
    st.markdown(
        '<div class="welcome"><div class="welcome-icon">💬</div><div class="welcome-title">How can I help you?</div><div class="welcome-text">Ask about available information or attach a PDF, DOCX, TXT or CSV and ask questions about it.</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### 💡 Try asking")
    suggestion_items = SUGGESTED_QUESTIONS[:4]
    cols = st.columns(2)
    for i, item in enumerate(suggestion_items):
        with cols[i % 2]:
            if st.button(f"{item.get('emoji','💡')} {item['text']}", key=f"suggest_{i}", use_container_width=True):
                st.session_state.pending_question = item["text"]
                st.rerun()

# Conversation display
for index, message in enumerate(current_chat.get("messages", [])):
    role = message.get("role", "assistant")
    content = message.get("content", "")
    with st.chat_message(role):
        if role == "user" and st.session_state.editing_index == index:
            edited = st.text_area("Edit your message", value=content, key=f"edit_text_{index}", height=120)
            ec1, ec2 = st.columns(2)
            with ec1:
                if st.button("Save & regenerate", key=f"save_edit_{index}", type="primary"):
                    edited = edited.strip()
                    if edited:
                        truncate_chat(current_chat, index)
                        st.session_state.editing_index = None
                        st.session_state.pending_question = edited
                        st.rerun()
            with ec2:
                if st.button("Cancel", key=f"cancel_edit_{index}"):
                    st.session_state.editing_index = None
                    st.rerun()
            continue

        st.markdown(content)
        if role == "user":
            a, b = st.columns([1, 1])
            with a:
                if st.button("✏️ Edit", key=f"edit_{index}", use_container_width=True):
                    st.session_state.editing_index = index
                    st.rerun()
            with b:
                if st.button("📋 Copy", key=f"copy_user_{index}", use_container_width=True):
                    st.session_state.copy_text = content
                    st.toast("Message ready to copy")
        else:
            a, b, c, d, e = st.columns([1.15, 1.85, 0.8, 0.8, 4.4])
            with a:
                if st.button("📋 Copy", key=f"copy_ai_{index}", use_container_width=True):
                    st.session_state.copy_text = content
                    st.toast("Response copied to the copy panel")
            with b:
                if st.button("🔄 Regenerate", key=f"regen_{index}", use_container_width=True):
                    if index > 0 and current_chat["messages"][index - 1].get("role") == "user":
                        remove_message(current_chat, index)
                        st.session_state.pending_regenerate = current_chat["messages"][index - 1].get("content", "")
                        st.rerun()
            with c:
                feedback = message.get("feedback")
                if st.button("👍" if feedback != "positive" else "👍✓", key=f"up_{index}"):
                    update_message_feedback(current_chat, index, None if feedback == "positive" else "positive")
                    refresh_chats(); st.rerun()
            with d:
                feedback = message.get("feedback")
                if st.button("👎" if feedback != "negative" else "👎✓", key=f"down_{index}"):
                    update_message_feedback(current_chat, index, None if feedback == "negative" else "negative")
                    refresh_chats(); st.rerun()
            if message.get("sources"):
                render_sources(message["sources"])

if st.session_state.get("copy_text"):
    with st.popover("📋 Copy response", use_container_width=True):
        st.text_area("", st.session_state.copy_text, height=150, label_visibility="collapsed")
        if st.button("Close", use_container_width=True):
            st.session_state.copy_text = None
            st.rerun()

# File upload composer area
with st.expander("＋ Attach files", expanded=False):
    uploaded_files = st.file_uploader(
        "PDF, DOCX, TXT or CSV",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Files are processed automatically and scoped to this conversation.",
    )
    if uploaded_files:
        signature = get_attachment_signature(uploaded_files)
        key = f"processed_upload_{current_chat_id}"
        if st.session_state.get(key) != signature:
            st.session_state[key] = signature
            with st.spinner("Processing attached files..."):
                result = add_conversation_files(current_chat_id, uploaded_files)
            for record in result.get("added", []):
                st.success(f"📄 {record['file_name']} is ready.")
            for record in result.get("skipped", []):
                st.info(f"📄 {record['name']} is already attached.")
            for error in result.get("errors", []):
                st.error(error)
            if result.get("added"):
                st.rerun()


def process_question(question, save_user=True):
    question = str(question or "").strip()
    if not question:
        return
    if save_user:
        add_message(current_chat, "user", question)
    start = time.perf_counter()
    try:
        with st.chat_message("assistant"):
            stream, sources = get_qa_stream(
                question,
                chat_history=current_chat["messages"][:-1] if save_user else current_chat["messages"],
                chat_id=current_chat_id,
                temperature=st.session_state.temperature,
            )
            answer = st.write_stream(stream)
            answer = str(answer or "").strip()
            elapsed = time.perf_counter() - start
            if sources:
                render_sources(sources)
        add_message(current_chat, "assistant", answer, sources=sources, response_time=elapsed)
        refresh_chats()
    except Exception as error:
        elapsed = time.perf_counter() - start
        text = str(error)
        if "429" in text or "RESOURCE_EXHAUSTED" in text:
            answer = "⚠️ **AI service temporarily unavailable**\n\nThe Gemini API usage limit has been reached. Please try again later."
        else:
            answer = "⚠️ **Something went wrong while processing your request.**\n\nPlease try again."
        add_message(current_chat, "assistant", answer, response_time=elapsed)
        st.error(answer)
        refresh_chats()

# Pending operations are intentionally handled after the current history is rendered.
if st.session_state.pending_regenerate:
    question = st.session_state.pending_regenerate
    st.session_state.pending_regenerate = None
    process_question(question, save_user=False)
    st.rerun()

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(question, save_user=True)
    st.rerun()

user_question = st.chat_input("Message AI Customer Support...")
if user_question:
    process_question(user_question, save_user=True)
    st.rerun()
