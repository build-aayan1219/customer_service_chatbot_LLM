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
    add_conversation_file_payloads,
    compare_uploaded_evidence_with_message,
    delete_all_conversation_files,
    delete_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)
from src.config import LLM_CONFIG, SUGGESTED_QUESTIONS, KB_PIPELINE_CONFIG, TASK2_CONFIG
from src.background_queue import get_job, run_with_timeout, cleanup_old_jobs
from src.retention_manager import cleanup_expired_files
from src.knowledge_base import run_scheduled_knowledge_base_pipeline, render_knowledge_base

st.set_page_config(
    page_title="Claude",
    page_icon="✻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Claude Precise Dark Theme Stylesheet
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
<<<<<<< HEAD
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Claude Exact Dark Background */
.stApp {
    background-color: #1e1e1e !important;
    color: #e3e2de !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 6.5rem !important;
    max-width: 820px !important;
}

/* Sidebar Styling: Claude Dark */
[data-testid="stSidebar"] {
    background-color: #181818 !important;
    border-right: 1px solid #282828 !important;
    padding-top: 1rem !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #b5b3ad !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #262626 !important;
    color: #ffffff !important;
}

/* Claude Sidebar Brand */
.claude-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px 14px 12px;
    font-size: 1.15rem;
    font-weight: 600;
    color: #f5f5f4;
    letter-spacing: -0.01em;
}
.claude-star-icon {
    color: #d97757;
    font-size: 1.25rem;
}

/* Claude New Chat Button */
.claude-new-btn button {
    background-color: #2b2b2b !important;
    border: 1px solid #3d3d3d !important;
    color: #f5f5f4 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 14px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}
.claude-new-btn button:hover {
    background-color: #353535 !important;
    border-color: #4f4f4f !important;
}

/* Section Header in Sidebar */
.claude-section-title {
    font-size: 0.76rem;
    font-weight: 600;
    color: #78756e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 14px 12px 6px 12px;
}

/* User Profile Badge at Sidebar Bottom */
.claude-user-profile {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    margin-top: 20px;
    border-top: 1px solid #282828;
    color: #b5b3ad;
    font-size: 0.85rem;
}
.claude-avatar {
    width: 24px;
    height: 24px;
    background: #d97757;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
}

/* Claude Hero Screen */
.claude-hero-container {
    text-align: center;
    padding: 7rem 1.5rem 3rem 1.5rem;
    max-width: 680px;
    margin: 0 auto;
}
.claude-sunburst {
    color: #d97757;
    font-size: 2.2rem;
    display: inline-block;
    margin-right: 10px;
    vertical-align: middle;
}
.claude-greeting {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 2.85rem;
    font-weight: 400;
    color: #ecebe6;
    letter-spacing: -0.02em;
    display: inline-block;
    vertical-align: middle;
}

/* Claude Floating Chat Card */
.claude-chat-box {
    background: #2b2a27;
    border: 1px solid #3c3a35;
    border-radius: 20px;
    padding: 20px 24px;
    margin: 20px auto;
    max-width: 760px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

/* Top Banner Badge */
.claude-plan-badge {
    text-align: center;
    margin-bottom: 24px;
}
.claude-plan-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #2b2a27;
    border: 1px solid #3d3b36;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    color: #a39e93;
}
.claude-plan-pill a {
    color: #d97757;
    text-decoration: none;
    font-weight: 500;
}

/* Claude Chat Message Styling */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 1rem 0.5rem !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #292825 !important;
    border-radius: 16px !important;
    padding: 0.9rem 1.25rem !important;
    border: 1px solid #383631 !important;
    margin-bottom: 1.2rem !important;
}

/* Claude Bottom Status Pill */
.claude-footer-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.78rem;
    color: #8c8577;
    padding: 6px 2px;
}
.claude-model-select {
    color: #e3e2de;
    font-weight: 500;
=======
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    color: #0F172A;
    background-color: #FAFAFC;
}

.block-container {
    padding-top: 1.25rem;
    padding-bottom: 7rem;
    max-width: 920px;
}

/* Status Indicator Dot */
.status-dot {
    height: 8px;
    width: 8px;
    background-color: #22C55E;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}

/* App Bar & Title */
.title {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: #0F172A;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.subtitle {
    color: #64748B;
    font-size: 0.825rem;
    margin-top: 2px;
    margin-bottom: 16px;
    font-weight: 400;
}

/* Sidebar Drawer */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}

.sidebar-brand {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #0F172A;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

section[data-testid="stSidebar"] h3 {
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748B !important;
    font-weight: 600 !important;
    margin-top: 18px !important;
    margin-bottom: 8px !important;
}

section[data-testid="stSidebar"] div.stButton > button {
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    background-color: #FFFFFF;
    color: #1E293B;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.15s ease;
    padding: 8px 12px;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #F1F5F9;
    border-color: #CBD5E1;
    color: #0F172A;
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background-color: #0F172A;
    color: #FFFFFF;
    border: none;
    font-weight: 600;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
    background-color: #1E293B;
}

/* ChatGPT / Claude Empty State Home */
.welcome-hero {
    max-width: 620px;
    margin: 40px auto 28px;
    text-align: center;
}

.welcome-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    background-color: #F1F5F9;
    border: 1px solid #E2E8F0;
    font-size: 0.78rem;
    font-weight: 600;
    color: #475569;
    margin-bottom: 14px;
}

.welcome-title {
    font-size: 1.75rem;
    font-weight: 750;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin: 8px 0;
    line-height: 1.25;
}

.welcome-text {
    color: #64748B;
    font-size: 0.9rem;
    line-height: 1.6;
    margin-bottom: 24px;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    padding: 16px 20px;
    border-radius: 16px;
    margin-bottom: 14px;
    border: 1px solid #E2E8F0;
    background-color: #FFFFFF;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
    background-color: #F8FAFC;
    border-color: #E2E8F0;
}

/* Modern Input Composer */
div[data-testid="stChatInput"] {
    border-radius: 16px;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #2563EB;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

/* Source Group & Citations */
.source-group {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 8px 0;
    background-color: #F8FAFC;
}

.source-file {
    font-weight: 600;
    font-size: 0.85rem;
    color: #1E293B;
}

.source-meta {
    font-size: 0.75rem;
    color: #64748B;
    margin-top: 2px;
}

.source-section {
    font-size: 0.8rem;
    margin-top: 8px;
    padding-top: 6px;
    border-top: 1px solid #E2E8F0;
}

/* File Cards */
.file-card {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    background-color: #FFFFFF;
}

.small-muted {
    font-size: 0.75rem;
    color: #64748B;
}

.stat-card {
    padding: 16px;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    background-color: #FFFFFF;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

/* Custom button touch target & hover transitions */
div.stButton > button {
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.15s ease-in-out;
}

div.stButton > button:hover {
    border-color: #CBD5E1;
    background-color: #F8FAFC;
>>>>>>> 6822f041b6221efdc478e0ee8d93ceae6c3d2c70
}
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
    if "show_kb" not in st.session_state:
        st.session_state.show_kb = False
    if "show_settings_modal" not in st.session_state:
        st.session_state.show_settings_modal = False
    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None
    if "pending_regenerate" not in st.session_state:
        st.session_state.pending_regenerate = None
    if "temperature" not in st.session_state:
        st.session_state.temperature = float(LLM_CONFIG.get("temperature", 0.1))
    if "task2_jobs" not in st.session_state:
        st.session_state.task2_jobs = []

init_state()

# Run maintenance routines once per server startup session
if "app_startup_done" not in st.session_state:
    st.session_state.app_startup_done = True
    if KB_PIPELINE_CONFIG.get("auto_run_on_app_start", False):
        try:
            run_scheduled_knowledge_base_pipeline()
        except Exception:
            pass
    try:
        cleanup_expired_files()
        cleanup_old_jobs(int(TASK2_CONFIG.get("background_job_retention_hours", 24)))
    except Exception:
        pass

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

    with st.expander(f"📚 Sources · {len(groups)} verified reference{'s' if len(groups) != 1 else ''}"):
        for (kind, name), items in groups.items():
            icon = "📄" if kind == "file" else "📚"
            section_label = "section" if len(items) == 1 else "sections"
            source_label = "Conversation file" if kind == "file" else "Knowledge Base"
            st.markdown(
                f'<div style="border: 1px solid #3d3b36; border-radius: 10px; padding: 10px 14px; margin: 6px 0; background: #262522;">'
                f'<div style="font-weight: 600; color: #ecebe6;">{icon} {name}</div>'
                f'<div style="font-size: 0.78rem; color: #9c978b;">{len(items)} relevant {section_label} · {source_label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            for number, (content, metadata) in enumerate(items, start=1):
                section = metadata.get("section") or metadata.get("location") or "Relevant section"
                with st.expander(f"{section}", expanded=False):
                    st.write(content)

def export_markdown(chat):
    lines = [f"# {chat.get('title', 'Conversation')}", "", f"Created: {chat.get('created_at', '')}", ""]
    for message in chat.get("messages", []):
        role = "You" if message.get("role") == "user" else "Claude"
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
    st.session_state.show_kb = False
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

# -----------------------------------------------------------------------------
# Claude Precise Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="claude-brand">
            <span class="claude-star-icon">✻</span>
            <span>Claude</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="claude-new-btn">', unsafe_allow_html=True)
    if st.button("＋  New chat", key="new_chat_btn", use_container_width=True):
        new_chat()
    st.markdown('</div>', unsafe_allow_html=True)

    search = st.text_input("Search", value=st.session_state.search_text, placeholder="🔍 Search...", label_visibility="collapsed")
    st.session_state.search_text = search

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("📁 Projects", use_container_width=True):
            st.session_state.show_dashboard = not st.session_state.show_dashboard
            st.session_state.show_kb = False
            st.rerun()
    with col_s2:
        if st.button("📚 Artifacts", use_container_width=True):
            st.session_state.show_kb = not st.session_state.show_kb
            st.session_state.show_dashboard = False
            st.rerun()

    if st.button("⚙️ Settings Modal", use_container_width=True):
        st.session_state.show_settings_modal = not st.session_state.show_settings_modal
        st.rerun()

    st.markdown('<div class="claude-section-title">Pinned</div>', unsafe_allow_html=True)
    visible = [c for c in search_chats(st.session_state.chats, search) if st.session_state.show_archived or not c.get("archived", False)]
    pinned = [c for c in visible if c.get("pinned")]
    regular = [c for c in visible if not c.get("pinned")]

    if pinned:
        for chat in pinned:
            label = ("🟢 " if chat["id"] == current_chat_id else "📌 ") + chat.get("title", "New Chat")
            if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.show_dashboard = False
                st.session_state.show_kb = False
                st.rerun()
    else:
        st.caption("No pinned chats.")

    st.markdown('<div class="claude-section-title">Recents</div>', unsafe_allow_html=True)
    if regular:
        for chat in regular[:15]:
            label = ("🟢 " if chat["id"] == current_chat_id else "💬 ") + chat.get("title", "New Chat")
            if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.show_dashboard = False
                st.session_state.show_kb = False
                st.rerun()
    else:
        st.caption("No recent conversations.")

    st.markdown(
        """
        <div class="claude-user-profile">
            <div class="claude-avatar">A</div>
            <div>
                <div style="font-weight: 600; color: #ecebe6;">Aayan Shaikh</div>
                <div style="font-size: 0.72rem; color: #78756e;">Free plan · Upgrade</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Claude Precise Settings Dialog (Matches Screen 2)
# -----------------------------------------------------------------------------
if st.session_state.show_settings_modal:
    with st.expander("⚙️ Claude Settings (General · Appearance · Voice · Capabilities)", expanded=True):
        st.markdown("### Settings")
        set_col1, set_col2 = st.columns([1, 2])
        with set_col1:
            st.markdown(
                """
                **Preferences**
                - ⚙️ General
                - 👤 Account
                - 🛡️ Privacy
                - 💳 Billing
                - 💡 Capabilities
                - 🧠 Memory
                - 🪞 Reflect
                - ⏱️ Time and focus
                - `</>` Claude Code
                """
            )
        with set_col2:
            st.markdown("##### **Appearance**")
            st.selectbox("Theme", ["System", "Dark", "Light"], index=1)
            st.selectbox("Interface font", ["Default · Anthropic Sans", "Inter", "System Sans"], index=0)
            st.selectbox("Response font", ["Anthropic Serif", "Plus Jakarta Sans", "JetBrains Mono"], index=0)
            st.selectbox("Transcript text size", ["Small", "Medium", "Large"], index=1)
            st.selectbox("Transcript width", ["Narrow", "Medium", "Wide"], index=0)
            st.selectbox("Motion", ["System", "Reduced", "Full"], index=0)

            st.markdown("##### **Voice**")
            st.selectbox("Language", ["English", "Hindi", "Spanish", "French"], index=0)
            st.selectbox("Style", ["Buttery", "Clear", "Warm", "Direct"], index=0)
            st.selectbox("Speed", ["Normal", "Fast", "Relaxed"], index=0)

        if st.button("Close Settings", type="primary"):
            st.session_state.show_settings_modal = False
            st.rerun()

# Navigation routing
if st.session_state.show_dashboard:
    from src.analytics import render_analytics
    render_analytics()
    if st.button("← Return to Claude Chat"):
        st.session_state.show_dashboard = False
        st.rerun()
    st.stop()

if st.session_state.show_kb:
    render_knowledge_base()
    if st.button("← Return to Claude Chat"):
        st.session_state.show_kb = False
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# Main Chat Area: Claude Experience
# -----------------------------------------------------------------------------

# Top Banner Pill
st.markdown(
    """
    <div class="claude-plan-badge">
        <div class="claude-plan-pill">
            <span>Free plan · </span>
            <a href="#">Upgrade</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Empty State: "Hello, night owl" / "Good day"
if not current_chat["messages"]:
    hour = datetime.now().hour
    time_greeting = "Hello, night owl" if (hour >= 21 or hour < 5) else ("Good morning" if hour < 12 else "Good afternoon")
    st.markdown(
        f"""
        <div class="claude-hero-container">
            <span class="claude-sunburst">✻</span>
            <div class="claude-greeting">{time_greeting}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Claude Quick Starters
    suggestion_items = SUGGESTED_QUESTIONS[:4]
    cols = st.columns(2)
    for i, item in enumerate(suggestion_items):
        with cols[i % 2]:
            if st.button(f"{item.get('emoji','💡')}  {item['text']}", key=f"suggest_{i}", use_container_width=True):
                st.session_state.pending_question = item["text"]
                st.rerun()

# Attached Files Area
files = list_conversation_files(current_chat_id)
if files:
    with st.expander(f"📎 Attached files ({len(files)})", expanded=False):
        for record in files:
            file_id = record.get("id")
            name = record.get("file_name", "Attached file")
            size = record.get("size_bytes", record.get("size", 0))
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**📄 {name}** ({size / 1024:.1f} KB)")
            with col2:
                if st.button("Remove", key=f"remove_file_{file_id}"):
                    remove_conversation_file(current_chat_id, file_id)
                    st.rerun()

# Conversation display

for index, message in enumerate(current_chat.get("messages", [])):
    role = message.get("role", "assistant")
    content = message.get("content", "")
    with st.chat_message(role):
        st.markdown(content)
        if role == "assistant":
            col_a1, col_a2, col_a3 = st.columns([1, 1, 8])
            with col_a1:
                feedback = message.get("feedback")
                if st.button("👍" if feedback != "positive" else "👍✓", key=f"up_{index}"):
                    update_message_feedback(current_chat, index, None if feedback == "positive" else "positive")
                    refresh_chats(); st.rerun()
            with col_a2:
                if st.button("👎" if feedback != "negative" else "👎✓", key=f"down_{index}"):
                    update_message_feedback(current_chat, index, None if feedback == "negative" else "negative")
                    refresh_chats(); st.rerun()
            if message.get("sources"):
                render_sources(message["sources"])

# Claude Floating Attachment & Input Dock
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
dock_c1, dock_c2, dock_c3 = st.columns([1.5, 6, 2.5])
with dock_c1:
    with st.popover("＋ Attach"):
        st.markdown("##### **Attach Files**")
        uploaded_files = st.file_uploader(
            "Evidence / Docs",
            type=["pdf", "docx", "txt", "csv", "png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
with dock_c2:
    st.markdown('<div class="claude-footer-meta"><span>Project: Customer Service KB</span> · <span class="claude-model-select">Claude 3.7 Sonnet</span></div>', unsafe_allow_html=True)
with dock_c3:
    if st.button("🗑️ Clear Context", use_container_width=True):
        delete_conversation_files(current_chat_id)
        st.rerun()

if "uploaded_files" in locals() and uploaded_files:
    signature = get_attachment_signature(uploaded_files)
    key = f"processed_upload_{current_chat_id}"
    if st.session_state.get(key) != signature:
        st.session_state[key] = signature
        payloads = [{"name": item.name, "original_name": item.name, "data": item.getvalue()} for item in uploaded_files]
        with st.spinner("Processing evidence..."):
            job = run_with_timeout(
                add_conversation_file_payloads,
                current_chat_id,
                payloads,
                timeout_seconds=int(TASK2_CONFIG.get("processing_timeout_seconds", 30)),
                description="Evidence processing",
            )
        if job.get("status") == "completed":
            st.success("Files attached successfully.")
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
            if sources:
                render_sources(sources)

            elapsed = time.perf_counter() - start
            st.markdown(
                f'<div style="margin-top: 6px; display: flex; align-items: center; gap: 8px;">'
                f'<span style="font-family: \'JetBrains Mono\'; font-size: 0.74rem; color: #8c8577; background: #2b2a27; padding: 2px 8px; border-radius: 4px;">⚡ {elapsed:.2f}s</span>'
                f'<span style="font-size: 0.74rem; color: #8c8577; background: #2b2a27; padding: 2px 8px; border-radius: 4px;">Claude 3.7 Sonnet · Verified Grounding</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        add_message(current_chat, "assistant", answer, sources=sources, response_time=elapsed)
        refresh_chats()
    except Exception as error:
        elapsed = time.perf_counter() - start
        answer = "⚠️ **Something went wrong while processing your request.** Please try again."
        add_message(current_chat, "assistant", answer, response_time=elapsed)
        st.error(answer)
        refresh_chats()

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(question, save_user=True)
    st.rerun()

user_question = st.chat_input("How can I help you today?")
if user_question:
    process_question(user_question, save_user=True)
    st.rerun()
