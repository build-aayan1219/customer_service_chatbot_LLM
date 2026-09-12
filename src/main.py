import html
import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.chat_manager import (
    add_message,
    create_chat,
    delete_chat,
    find_chat,
    load_chats,
    rename_chat,
    search_chats,
    set_chat_archived,
    set_chat_pinned,
    truncate_chat,
    update_message_feedback,
)
from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    list_conversation_files,
    remove_conversation_file,
)
from src.langchain_helper import get_qa_stream


st.set_page_config(
    page_title="AI Customer Service Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
    .stApp {
        background: #f7f8fc;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8eaf0;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    .app-title {
        font-size: 1.55rem;
        font-weight: 750;
        letter-spacing: -0.03em;
        margin-bottom: 0.1rem;
    }

    .app-subtitle {
        color: #6b7280;
        font-size: 0.84rem;
        margin-bottom: 1rem;
    }

    .chat-context {
        border: 1px solid #dfe3ec;
        background: #ffffff;
        border-radius: 12px;
        padding: 10px 13px;
        margin: 8px 0 14px 0;
        font-size: 0.84rem;
    }

    .chat-context strong {
        font-size: 0.88rem;
    }

    .chat-context span {
        color: #6b7280;
    }

    .source-group {
        border: 1px solid #e4e7ee;
        border-radius: 12px;
        padding: 11px 13px;
        margin-bottom: 8px;
        background: #ffffff;
    }

    .source-file {
        font-weight: 650;
        font-size: 0.91rem;
    }

    .source-meta {
        color: #6b7280;
        font-size: 0.76rem;
        margin-top: 3px;
    }

    .welcome {
        text-align: center;
        padding: 4rem 1rem 1.5rem 1rem;
    }

    .welcome-icon {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }

    .welcome-title {
        font-size: 1.7rem;
        font-weight: 750;
        letter-spacing: -0.03em;
    }

    .welcome-text {
        color: #6b7280;
        max-width: 650px;
        margin: 0.45rem auto 0 auto;
        line-height: 1.55;
    }

    .metric-card {
        border: 1px solid #e4e7ee;
        background: #ffffff;
        border-radius: 14px;
        padding: 15px;
        min-height: 105px;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.8rem;
    }

    .metric-value {
        font-size: 1.55rem;
        font-weight: 750;
        margin-top: 3px;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.78rem;
    }

    .sidebar-chat-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .stChatMessage {
        border-radius: 14px;
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 0.7rem;
    }

    .settings-box {
        border: 1px solid #e4e7ee;
        background: #ffffff;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_state():
    if "current_chat_id" not in st.session_state:
        chats = load_chats()
        if chats:
            st.session_state.current_chat_id = chats[0]["id"]
        else:
            chat = create_chat()
            st.session_state.current_chat_id = chat["id"]

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.2

    if "dashboard_open" not in st.session_state:
        st.session_state.dashboard_open = False

    if "copy_text" not in st.session_state:
        st.session_state.copy_text = None


initialize_state()


def get_current_chat():
    chat_id = st.session_state.current_chat_id
    chat = find_chat(chat_id)

    if chat is None:
        chats = load_chats()
        if chats:
            st.session_state.current_chat_id = chats[0]["id"]
            return chats[0]

        chat = create_chat()
        st.session_state.current_chat_id = chat["id"]
        return chat

    return chat


def clean_source(source):
    if isinstance(source, dict):
        content = source.get("content", "")
        metadata = source.get("metadata", {})
        return content, metadata

    content = getattr(source, "page_content", str(source))
    metadata = getattr(source, "metadata", {})
    return content, metadata


def source_group_key(metadata):
    source_type = metadata.get("source_type", "global_knowledge")

    if source_type == "conversation_file":
        name = (
            metadata.get("source_file")
            or metadata.get("file_name")
            or metadata.get("filename")
            or "Conversation file"
        )
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

    source_count = len(groups)
    source_label = "source" if source_count == 1 else "sources"

    with st.expander(f"📚 Sources · {source_count} {source_label}"):
        for (kind, name), items in groups.items():
            icon = "📄" if kind == "file" else "📚"
            section_label = "section" if len(items) == 1 else "sections"
            source_label = (
                "Conversation file" if kind == "file" else "Knowledge Base"
            )

            st.markdown(
                f'<div class="source-group">'
                f'<div class="source-file">{icon} {html.escape(str(name))}</div>'
                f'<div class="source-meta">{len(items)} relevant '
                f'{section_label} · {source_label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            for number, (content, metadata) in enumerate(items, start=1):
                section = (
                    metadata.get("section")
                    or metadata.get("location")
                    or "Relevant section"
                )

                with st.expander(str(section), expanded=False):
                    st.write(content)

                    extra = []

                    if (
                        metadata.get("location")
                        and metadata.get("location") != section
                    ):
                        extra.append(str(metadata["location"]))

                    if metadata.get("chunk_index") is not None:
                        extra.append(f"chunk {metadata['chunk_index']}")

                    if extra:
                        st.caption(" · ".join(extra))


def render_copy_controls(content, message_index):
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button(
            "📋 Copy",
            key=f"copy_{message_index}",
            use_container_width=True,
        ):
            st.session_state.copy_text = content
            st.toast("Response copied. Use the copy action from your browser if needed.")

    with col2:
        if st.button(
            "🔄 Regenerate",
            key=f"regenerate_{message_index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = content
            st.session_state.regenerate_index = message_index
            st.rerun()

    with col3:
        if st.button(
            "✏️ Edit",
            key=f"edit_{message_index}",
            use_container_width=True,
        ):
            st.session_state.editing_index = message_index
            st.rerun()


def export_chat_markdown(chat):
    lines = [
        f"# {chat.get('title', 'Conversation')}",
        "",
        f"Created: {chat.get('created_at', '')}",
        "",
    ]

    for message in chat.get("messages", []):
        role = message.get("role", "assistant").capitalize()
        content = message.get("content", "")

        lines.append(f"## {role}")
        lines.append("")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def calculate_dashboard_metrics(chats):
    conversations = len(chats)
    questions = 0
    responses = 0
    total_response_time = 0.0
    response_count = 0
    positive = 0
    negative = 0

    for chat in chats:
        for message in chat.get("messages", []):
            role = message.get("role")

            if role == "user":
                questions += 1

            elif role == "assistant":
                responses += 1

                response_time = message.get("response_time")

                if response_time is not None:
                    try:
                        total_response_time += float(response_time)
                        response_count += 1
                    except (TypeError, ValueError):
                        pass

                feedback = message.get("feedback")

                if feedback == "positive":
                    positive += 1
                elif feedback == "negative":
                    negative += 1

    average_response_time = (
        total_response_time / response_count
        if response_count
        else 0
    )

    feedback_total = positive + negative

    satisfaction = (
        (positive / feedback_total) * 100
        if feedback_total
        else 0
    )

    return {
        "conversations": conversations,
        "questions": questions,
        "responses": responses,
        "average_response_time": average_response_time,
        "satisfaction": satisfaction,
        "positive": positive,
        "negative": negative,
    }


def process_question(question):
    question = question.strip()

    if not question:
        return

    current_chat = get_current_chat()
    chat_id = current_chat["id"]

    add_message(
        chat_id,
        "user",
        question,
    )

    st.session_state.pending_question = None

    current_chat = find_chat(chat_id)

    history = current_chat["messages"][:-1]

    answer_placeholder = st.empty()
    start_time = time.time()

    full_response = ""

    try:
        stream, sources = get_qa_stream(
            question,
            chat_history=history,
            chat_id=chat_id,
            temperature=st.session_state.temperature,
        )

        with answer_placeholder.container():
            with st.chat_message("assistant"):
                full_response = st.write_stream(stream)

        if not isinstance(full_response, str):
            full_response = "".join(str(part) for part in full_response)

        elapsed = time.time() - start_time

        add_message(
            chat_id,
            "assistant",
            full_response,
            sources=sources,
            response_time=elapsed,
        )

        st.rerun()

    except Exception as exc:
        error_text = str(exc)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            error_message = (
                "⚠️\n\n"
                "**AI service temporarily unavailable**\n\n"
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )
        else:
            error_message = (
                "⚠️ **Something went wrong while generating the response.**\n\n"
                f"`{error_text}`"
            )

        with answer_placeholder.container():
            st.chat_message("assistant").markdown(error_message)


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:
    st.markdown(
        '<div class="app-title">🤖 AI Support</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">Intelligent customer service assistant</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "➕ New Chat",
        use_container_width=True,
        type="primary",
    ):
        chat = create_chat()
        st.session_state.current_chat_id = chat["id"]
        st.session_state.dashboard_open = False
        st.session_state.pending_question = None
        st.session_state.editing_index = None
        st.rerun()

    st.divider()

    if st.button(
        "📊 Dashboard",
        use_container_width=True,
    ):
        st.session_state.dashboard_open = True
        st.rerun()

    if st.button(
        "💬 Conversations",
        use_container_width=True,
    ):
        st.session_state.dashboard_open = False
        st.rerun()

    st.markdown("### 🔎 Search")

    search_value = st.text_input(
        "Search conversations",
        value=st.session_state.search_query,
        placeholder="Search chats...",
        label_visibility="collapsed",
    )

    if search_value != st.session_state.search_query:
        st.session_state.search_query = search_value

    all_chats = load_chats()

    if st.session_state.search_query.strip():
        visible_chats = search_chats(
            st.session_state.search_query.strip()
        )
    else:
        visible_chats = all_chats

    pinned_chats = [
        chat for chat in visible_chats
        if chat.get("pinned")
    ]

    regular_chats = [
        chat for chat in visible_chats
        if not chat.get("pinned")
    ]

    if pinned_chats:
        st.markdown("### 📌 Pinned")

        for chat in pinned_chats:
            title = chat.get("title") or "New Conversation"

            if st.button(
                f"📌 {title}",
                key=f"pinned_chat_{chat['id']}",
                use_container_width=True,
            ):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.dashboard_open = False
                st.rerun()

    st.markdown("### 💬 Recent Chats")

    if not regular_chats and not pinned_chats:
        st.caption("No conversations found.")

    for chat in regular_chats:
        title = chat.get("title") or "New Conversation"

        button_text = f"{title}"

        if chat.get("archived"):
            button_text = f"🗃️ {button_text}"

        if st.button(
            button_text,
            key=f"chat_{chat['id']}",
            use_container_width=True,
        ):
            st.session_state.current_chat_id = chat["id"]
            st.session_state.dashboard_open = False
            st.rerun()

    st.divider()

    st.markdown("### ⚙️ Settings")

    temperature = st.slider(
        "Response creativity",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.temperature),
        step=0.1,
        help="Lower values are more deterministic. Higher values are more creative.",
    )

    st.session_state.temperature = temperature

    current_chat = get_current_chat()

    if st.button(
        "📥 Export Current Chat",
        use_container_width=True,
    ):
        markdown = export_chat_markdown(current_chat)

        st.download_button(
            "Download Markdown",
            data=markdown,
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button(
        "🗑️ Delete Current Chat",
        use_container_width=True,
    ):
        delete_chat(current_chat["id"])
        delete_all_conversation_files(current_chat["id"])

        remaining = load_chats()

        if remaining:
            st.session_state.current_chat_id = remaining[0]["id"]
        else:
            new_chat = create_chat()
            st.session_state.current_chat_id = new_chat["id"]

        st.session_state.dashboard_open = False
        st.rerun()


# -------------------------
# Main content
# -------------------------

if st.session_state.dashboard_open:
    st.title("📊 Dashboard")
    st.caption("Overview of your local chatbot activity.")

    chats = load_chats()
    metrics = calculate_dashboard_metrics(chats)

    columns = st.columns(4)

    with columns[0]:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Conversations</div>'
            f'<div class="metric-value">{metrics["conversations"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with columns[1]:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Questions</div>'
            f'<div class="metric-value">{metrics["questions"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with columns[2]:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Avg. Response Time</div>'
            f'<div class="metric-value">{metrics["average_response_time"]:.2f}s</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with columns[3]:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Satisfaction</div>'
            f'<div class="metric-value">{metrics["satisfaction"]:.0f}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 👍 Feedback")

    feedback_columns = st.columns(2)

    with feedback_columns[0]:
        st.metric(
            "Positive",
            metrics["positive"],
        )

    with feedback_columns[1]:
        st.metric(
            "Negative",
            metrics["negative"],
        )

    st.stop()


current_chat = get_current_chat()

chat_title = current_chat.get("title") or "New Conversation"

title_col, action_col = st.columns([7, 1])

with title_col:
    st.markdown(
        f"## {html.escape(str(chat_title))}",
        unsafe_allow_html=True,
    )

with action_col:
    if current_chat.get("pinned"):
        pin_label = "📌 Unpin"
    else:
        pin_label = "📌 Pin"

    if st.button(
        pin_label,
        use_container_width=True,
    ):
        set_chat_pinned(
            current_chat["id"],
            not bool(current_chat.get("pinned")),
        )
        st.rerun()


files = list_conversation_files(current_chat["id"])

if files:
    file_count = len(files)
    file_label = "file" if file_count == 1 else "files"

    st.markdown(
        f'<div class="chat-context">'
        f'<strong>📎 {file_count} {file_label} attached</strong><br>'
        f'<span>Ask about the files directly — for example: '
        f'“What is the code related to?”</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.expander(
        f"📎 Attached files · {file_count}",
        expanded=False,
    ):
        for record in files:
            file_id = record.get("id")
            name = record.get("file_name", "Attached file")
            size = record.get("size", 0)
            chunks = record.get("chunk_count", 0)

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"**📄 {name}**")
                st.caption(
                    f"{size / 1024:.1f} KB · {chunks} chunks"
                )

            with col2:
                if st.button(
                    "Remove",
                    key=f"remove_file_{file_id}",
                ):
                    remove_conversation_file(
                        current_chat["id"],
                        file_id,
                    )
                    st.rerun()


if not current_chat["messages"]:
    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-icon">💬</div>'
        '<div class="welcome-title">How can I help you?</div>'
        '<div class="welcome-text">'
        'Ask about available information or attach a PDF, DOCX, TXT or CSV '
        'and ask questions about it.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Try asking")

    suggestion_items = [
        {
            "emoji": "📚",
            "text": "What information is available?",
        },
        {
            "emoji": "🔍",
            "text": "How can I solve a common issue?",
        },
        {
            "emoji": "📄",
            "text": "What is the code related to?",
        },
        {
            "emoji": "💬",
            "text": "What services do you provide?",
        },
    ]

    cols = st.columns(2)

    for i, item in enumerate(suggestion_items):
        with cols[i % 2]:
            if st.button(
                f"{item.get('emoji', '💡')} {item['text']}",
                key=f"suggest_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_question = item["text"]
                st.rerun()


# -------------------------
# Conversation display
# -------------------------

for index, message in enumerate(
    current_chat.get("messages", [])
):
    role = message.get("role", "assistant")
    content = message.get("content", "")

    with st.chat_message(role):
        if (
            role == "user"
            and st.session_state.editing_index == index
        ):
            edited = st.text_area(
                "Edit your message",
                value=content,
                key=f"edit_text_{index}",
                height=120,
            )

            edit_col1, edit_col2 = st.columns(2)

            with edit_col1:
                if st.button(
                    "Save & regenerate",
                    key=f"save_edit_{index}",
                    type="primary",
                    use_container_width=True,
                ):
                    edited = edited.strip()

                    if edited:
                        truncate_chat(
                            current_chat,
                            index,
                        )

                        st.session_state.editing_index = None
                        st.session_state.pending_question = edited
                        st.rerun()

            with edit_col2:
                if st.button(
                    "Cancel",
                    key=f"cancel_edit_{index}",
                    use_container_width=True,
                ):
                    st.session_state.editing_index = None
                    st.rerun()

        else:
            st.markdown(content)

            if role == "assistant":
                sources = message.get("sources", [])

                if sources:
                    render_sources(sources)

                feedback = message.get("feedback")

                feedback_col1, feedback_col2, feedback_col3 = st.columns(
                    [1, 1, 5]
                )

                with feedback_col1:
                    if st.button(
                        "👍",
                        key=f"positive_{index}",
                        use_container_width=True,
                    ):
                        update_message_feedback(
                            current_chat["id"],
                            message.get("id"),
                            "positive",
                        )
                        st.rerun()

                with feedback_col2:
                    if st.button(
                        "👎",
                        key=f"negative_{index}",
                        use_container_width=True,
                    ):
                        update_message_feedback(
                            current_chat["id"],
                            message.get("id"),
                            "negative",
                        )
                        st.rerun()

                with feedback_col3:
                    if feedback == "positive":
                        st.caption("👍 Thanks for the feedback!")
                    elif feedback == "negative":
                        st.caption("👎 Feedback recorded.")

                render_copy_controls(
                    content,
                    index,
                )


# -------------------------
# File uploader
# -------------------------

uploaded_files = st.file_uploader(
    "Attach files to this conversation",
    type=["pdf", "docx", "txt", "csv"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    help=(
        "Files are automatically processed and made available "
        "to this conversation."
    ),
)

if uploaded_files:
    try:
        add_conversation_files(
            current_chat["id"],
            uploaded_files,
        )
        st.rerun()
    except Exception as exc:
        st.error(
            f"Unable to process the uploaded file(s): {exc}"
        )


# -------------------------
# Pending question
# -------------------------

pending_question = st.session_state.pending_question

if pending_question:
    st.session_state.pending_question = None
    process_question(pending_question)


# -------------------------
# Chat input
# -------------------------

question = st.chat_input(
    "Message AI Support..."
)

if question:
    process_question(question)