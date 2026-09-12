import html
import time
from collections import defaultdict
from pathlib import Path

import streamlit as st

from src.chat_manager import (
    add_message,
    create_chat,
    delete_all_chats,
    delete_chat,
    find_chat,
    load_chats,
    rename_chat,
    search_chats,
    save_chat,
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

from src.langchain_helper import (
    get_qa_stream,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f7f8fc;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e6e8ef;
}

[data-testid="stSidebarContent"] {
    padding-top: 1rem;
}

.app-title {
    font-size: 1.55rem;
    font-weight: 750;
    letter-spacing: -0.03em;
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
    padding: 11px 14px;
    margin: 10px 0 14px 0;
    font-size: 0.84rem;
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

.file-card {
    border: 1px solid #e4e7ee;
    background: #ffffff;
    border-radius: 12px;
    padding: 11px 13px;
    margin-bottom: 7px;
}

.sidebar-section {
    margin-top: 0.5rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_chat_id" not in st.session_state:
    existing_chats = load_chats()

    if existing_chats:
        st.session_state.current_chat_id = (
            existing_chats[0]["id"]
        )

    else:
        new_chat = create_chat()
        save_chat(new_chat)

        st.session_state.current_chat_id = (
            new_chat["id"]
        )


if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False


if "search_text" not in st.session_state:
    st.session_state.search_text = ""


if "editing_index" not in st.session_state:
    st.session_state.editing_index = None


if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


if "upload_signature" not in st.session_state:
    st.session_state.upload_signature = ""


# ============================================================
# CHAT HELPERS
# ============================================================

def refresh_chats():
    st.session_state.chats = load_chats()

    return st.session_state.chats


def ensure_current_chat():
    chats = load_chats()

    current_id = st.session_state.get(
        "current_chat_id"
    )

    current_chat = (
        find_chat(
            chats,
            current_id,
        )
        if current_id
        else None
    )

    if current_chat is None:

        current_chat = create_chat()

        save_chat(
            current_chat
        )

        st.session_state.current_chat_id = (
            current_chat["id"]
        )

    return current_chat


def create_and_select_chat():
    new_chat = create_chat()

    save_chat(
        new_chat
    )

    st.session_state.current_chat_id = (
        new_chat["id"]
    )

    st.session_state.show_dashboard = False
    st.session_state.editing_index = None
    st.session_state.pending_question = None

    st.rerun()


# ============================================================
# SOURCE HELPERS
# ============================================================

def clean_source(source):
    if isinstance(
        source,
        dict,
    ):
        content = source.get(
            "page_content",
            source.get(
                "content",
                "",
            ),
        )

        metadata = source.get(
            "metadata",
            {},
        )

    else:
        content = getattr(
            source,
            "page_content",
            str(source),
        )

        metadata = getattr(
            source,
            "metadata",
            {},
        )

    if not isinstance(
        metadata,
        dict,
    ):
        metadata = {}

    return (
        str(content or ""),
        metadata,
    )


def source_group_key(metadata):
    source_type = (
        metadata.get(
            "source_type"
        )
        or metadata.get(
            "retrieval_source"
        )
    )

    if source_type == "conversation_file":

        filename = (
            metadata.get(
                "source_file"
            )
            or metadata.get(
                "file_name"
            )
            or metadata.get(
                "filename"
            )
            or "Attached file"
        )

        return (
            "file",
            Path(
                str(filename)
            ).name,
        )

    return (
        "global",
        "Knowledge Base",
    )


def render_sources(sources):
    if not sources:
        return

    groups = defaultdict(list)

    for source in sources:

        content, metadata = (
            clean_source(source)
        )

        groups[
            source_group_key(
                metadata
            )
        ].append(
            (
                content,
                metadata,
            )
        )

    group_count = len(groups)

    group_label = (
        "source"
        if group_count == 1
        else "sources"
    )

    with st.expander(
        f"📚 Sources · {group_count} {group_label}"
    ):

        for (
            group_key,
            items,
        ) in groups.items():

            kind, name = group_key

            icon = (
                "📄"
                if kind == "file"
                else "📚"
            )

            section_label = (
                "section"
                if len(items) == 1
                else "sections"
            )

            source_label = (
                "Conversation file"
                if kind == "file"
                else "Knowledge Base"
            )

            safe_name = html.escape(
                str(name)
            )

            st.markdown(
                f'<div class="source-group">'
                f'<div class="source-file">'
                f'{icon} {safe_name}'
                f'</div>'
                f'<div class="source-meta">'
                f'{len(items)} relevant '
                f'{section_label} · '
                f'{source_label}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            for (
                item_number,
                item,
            ) in enumerate(
                items,
                start=1,
            ):

                content, metadata = item

                section = (
                    metadata.get(
                        "section"
                    )
                    or metadata.get(
                        "location"
                    )
                    or (
                        f"Relevant section "
                        f"{item_number}"
                    )
                )

                section = str(
                    section
                )

                with st.expander(
                    section,
                    expanded=False,
                ):
                    st.write(
                        content
                    )


# ============================================================
# EXPORT
# ============================================================

def export_markdown(chat):
    title = str(
        chat.get(
            "title",
            "Conversation",
        )
    )

    lines = [
        f"# {title}",
        "",
        f"Created: {chat.get('created_at', '')}",
        "",
    ]

    for message in chat.get(
        "messages",
        [],
    ):

        role = str(
            message.get(
                "role",
                "assistant",
            )
        ).capitalize()

        content = str(
            message.get(
                "content",
                "",
            )
        )

        lines.extend(
            [
                f"## {role}",
                "",
                content,
                "",
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# DASHBOARD METRICS
# ============================================================

def dashboard_metrics(chats):
    questions = 0
    responses = 0
    positive = 0
    negative = 0
    response_times = []

    for chat in chats:

        for message in chat.get(
            "messages",
            [],
        ):

            role = message.get(
                "role"
            )

            if role == "user":

                questions += 1

            elif role == "assistant":

                responses += 1

                feedback = message.get(
                    "feedback"
                )

                if feedback == "positive":
                    positive += 1

                elif feedback == "negative":
                    negative += 1

                response_time = message.get(
                    "response_time"
                )

                if response_time is not None:

                    try:
                        response_times.append(
                            float(
                                response_time
                            )
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):
                        pass

    feedback_total = (
        positive
        + negative
    )

    satisfaction = (
        positive
        / feedback_total
        * 100
        if feedback_total
        else 0
    )

    average_time = (
        sum(response_times)
        / len(response_times)
        if response_times
        else 0
    )

    return {
        "chats": len(chats),
        "questions": questions,
        "responses": responses,
        "positive": positive,
        "negative": negative,
        "satisfaction": satisfaction,
        "average_time": average_time,
    }


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):
    question = str(
        question or ""
    ).strip()

    if not question:
        return

    chat = ensure_current_chat()

    chat_id = chat["id"]

    previous_history = list(
        chat.get(
            "messages",
            [],
        )
    )

    add_message(
        chat,
        "user",
        question,
    )

    updated_chats = load_chats()

    chat = find_chat(
        updated_chats,
        chat_id,
    )

    if chat is None:

        st.error(
            "The conversation could not be loaded. "
            "Please start a new chat."
        )

        return

    start_time = time.time()

    try:

        stream, sources = get_qa_stream(
            question,
            chat_history=previous_history,
            chat_id=chat_id,
        )

        with st.chat_message(
            "assistant"
        ):

            response = st.write_stream(
                stream
            )

        if not isinstance(
            response,
            str,
        ):

            response = "".join(
                str(part)
                for part in response
            )

        response = response.strip()

        elapsed = (
            time.time()
            - start_time
        )

        add_message(
            chat,
            "assistant",
            response,
            sources=sources,
            response_time=elapsed,
        )

        st.session_state.current_chat_id = (
            chat_id
        )

        st.session_state.chats = (
            load_chats()
        )

        st.rerun()

    except Exception as error:

        error_text = str(
            error
        )

        lower_error = (
            error_text.lower()
        )

        if (
            "429" in lower_error
            or "resource_exhausted"
            in lower_error
            or "quota" in lower_error
        ):

            st.error(
                "⚠️ AI service temporarily unavailable. "
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )

        else:

            st.error(
                "⚠️ Unable to generate a response."
            )

            st.caption(
                error_text
            )


# ============================================================
# CURRENT CHAT
# ============================================================

current_chat = ensure_current_chat()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="app-title">'
        '🤖 AI Support'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Intelligent customer service assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "➕ New Chat",
        use_container_width=True,
        type="primary",
    ):

        create_and_select_chat()

    if st.button(
        "📊 Dashboard",
        use_container_width=True,
    ):

        st.session_state.show_dashboard = True
        st.rerun()

    if st.button(
        "💬 Conversations",
        use_container_width=True,
    ):

        st.session_state.show_dashboard = False
        st.rerun()

    st.divider()

    st.markdown(
        "### 🔎 Search"
    )

    search_text = st.text_input(
        "Search conversations",
        value=st.session_state.search_text,
        placeholder="Search conversations...",
        label_visibility="collapsed",
    )

    st.session_state.search_text = (
        search_text
    )

    chats = load_chats()

    if search_text.strip():

        visible_chats = search_chats(
            chats,
            search_text,
        )

    else:

        visible_chats = chats

    pinned_chats = [
        chat
        for chat in visible_chats
        if chat.get("pinned")
    ]

    active_chats = [
        chat
        for chat in visible_chats
        if (
            not chat.get("pinned")
            and not chat.get("archived")
        )
    ]

    archived_chats = [
        chat
        for chat in visible_chats
        if chat.get("archived")
    ]

    if pinned_chats:

        st.markdown(
            "### 📌 Pinned"
        )

        for chat in pinned_chats:

            chat_title = str(
                chat.get(
                    "title",
                    "New Chat",
                )
            )

            button_label = (
                "📌 "
                + chat_title
            )

            if st.button(
                button_label,
                key=(
                    "pinned_chat_"
                    + chat["id"]
                ),
                use_container_width=True,
            ):

                st.session_state.current_chat_id = (
                    chat["id"]
                )

                st.session_state.show_dashboard = False

                st.rerun()

    st.markdown(
        "### 💬 Recent Chats"
    )

    if not active_chats:

        st.caption(
            "No active conversations."
        )

    for chat in active_chats:

        chat_title = str(
            chat.get(
                "title",
                "New Chat",
            )
        )

        if len(chat_title) > 34:
            chat_title = (
                chat_title[:31]
                + "..."
            )

        is_current = (
            chat["id"]
            == st.session_state.current_chat_id
        )

        if is_current:

            button_label = (
                "🟢 "
                + chat_title
            )

        else:

            button_label = (
                "💬 "
                + chat_title
            )

        if st.button(
            button_label,
            key=(
                "chat_"
                + chat["id"]
            ),
            use_container_width=True,
        ):

            st.session_state.current_chat_id = (
                chat["id"]
            )

            st.session_state.show_dashboard = False
            st.session_state.editing_index = None

            st.rerun()

    if archived_chats:

        with st.expander(
            f"🗃️ Archived · {len(archived_chats)}"
        ):

            for chat in archived_chats:

                chat_title = str(
                    chat.get(
                        "title",
                        "New Chat",
                    )
                )

                if len(chat_title) > 34:
                    chat_title = (
                        chat_title[:31]
                        + "..."
                    )

                if st.button(
                    chat_title,
                    key=(
                        "archived_"
                        + chat["id"]
                    ),
                    use_container_width=True,
                ):

                    st.session_state.current_chat_id = (
                        chat["id"]
                    )

                    st.session_state.show_dashboard = False

                    st.rerun()

    st.divider()

    st.markdown(
        "### ⚙️ Current Chat"
    )

    if current_chat.get(
        "pinned",
        False,
    ):

        pin_button_text = (
            "📌 Unpin Chat"
        )

    else:

        pin_button_text = (
            "📌 Pin Chat"
        )

    if st.button(
        pin_button_text,
        use_container_width=True,
    ):

        set_chat_pinned(
            current_chat,
            not bool(
                current_chat.get(
                    "pinned",
                    False,
                )
            ),
        )

        st.rerun()

    if current_chat.get(
        "archived",
        False,
    ):

        archive_button_text = (
            "📂 Unarchive Chat"
        )

    else:

        archive_button_text = (
            "🗃️ Archive Chat"
        )

    if st.button(
        archive_button_text,
        use_container_width=True,
    ):

        set_chat_archived(
            current_chat,
            not bool(
                current_chat.get(
                    "archived",
                    False,
                )
            ),
        )

        st.rerun()

    with st.expander(
        "✏️ Rename Chat"
    ):

        rename_title = st.text_input(
            "Chat title",
            value=current_chat.get(
                "title",
                "New Chat",
            ),
            key="rename_chat_title",
        )

        if st.button(
            "Save Title",
            key="save_chat_title",
            use_container_width=True,
        ):

            rename_chat(
                current_chat,
                rename_title,
            )

            st.rerun()

    with st.expander(
        "📥 Export"
    ):

        st.download_button(
            "Download Markdown",
            data=export_markdown(
                current_chat
            ),
            file_name=(
                "conversation.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button(
        "🗑️ Delete Chat",
        use_container_width=True,
    ):

        deleted_chat_id = (
            current_chat["id"]
        )

        remaining_chats = delete_chat(
            load_chats(),
            deleted_chat_id,
        )

        delete_all_conversation_files(
            [
                deleted_chat_id
            ]
        )

        if remaining_chats:

            st.session_state.current_chat_id = (
                remaining_chats[0]["id"]
            )

        else:

            replacement_chat = (
                create_chat()
            )

            save_chat(
                replacement_chat
            )

            st.session_state.current_chat_id = (
                replacement_chat["id"]
            )

        st.session_state.editing_index = None

        st.rerun()

    if st.button(
        "🧹 Clear All Chats",
        use_container_width=True,
    ):

        all_chats = load_chats()

        chat_ids = [
            chat["id"]
            for chat in all_chats
        ]

        delete_all_chats()

        if chat_ids:

            delete_all_conversation_files(
                chat_ids
            )

        replacement_chat = (
            create_chat()
        )

        save_chat(
            replacement_chat
        )

        st.session_state.current_chat_id = (
            replacement_chat["id"]
        )

        st.session_state.editing_index = None

        st.rerun()

    st.divider()

    st.markdown(
        "### ℹ️ About"
    )

    st.caption(
        "This AI Customer Support Assistant "
        "uses Retrieval-Augmented Generation "
        "(RAG) to answer questions using "
        "trusted knowledge and files attached "
        "to the current conversation."
    )

    st.markdown(
        "### 🛠️ Tech Stack"
    )

    st.caption(
        "Python • Streamlit • LangChain • Gemini "
        "• HuggingFace Embeddings • FAISS • SQLite"
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.show_dashboard:

    chats = load_chats()

    metrics = dashboard_metrics(
        chats
    )

    st.markdown(
        '<div class="app-title">'
        '📊 Analytics Dashboard'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Overview of chatbot activity and conversation performance'
        '</div>',
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(
        4
    )

    metric_values = [
        (
            "Conversations",
            metrics["chats"],
        ),
        (
            "Questions",
            metrics["questions"],
        ),
        (
            "AI Responses",
            metrics["responses"],
        ),
        (
            "Avg. Response",
            f'{metrics["average_time"]:.2f}s',
        ),
    ]

    for column, item in zip(
        metric_columns,
        metric_values,
    ):

        label, value = item

        with column:

            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">'
                f'{html.escape(str(label))}'
                f'</div>'
                f'<div class="metric-value">'
                f'{html.escape(str(value))}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        "### 👍 Feedback"
    )

    feedback_columns = st.columns(
        3
    )

    feedback_values = [
        (
            "Positive",
            metrics["positive"],
        ),
        (
            "Negative",
            metrics["negative"],
        ),
        (
            "Satisfaction",
            f'{metrics["satisfaction"]:.0f}%',
        ),
    ]

    for column, item in zip(
        feedback_columns,
        feedback_values,
    ):

        label, value = item

        with column:
            st.metric(
                label,
                value,
            )

    st.markdown(
        "### 💬 Recent Conversations"
    )

    for chat in chats[:10]:

        title = str(
            chat.get(
                "title",
                "New Chat",
            )
        )

        messages = chat.get(
            "messages",
            [],
        )

        user_count = sum(
            1
            for message in messages
            if message.get(
                "role"
            ) == "user"
        )

        assistant_count = sum(
            1
            for message in messages
            if message.get(
                "role"
            ) == "assistant"
        )

        st.markdown(
            f"**💬 {title}**"
        )

        st.caption(
            f"{user_count} questions • "
            f"{assistant_count} AI responses"
        )

    st.stop()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="app-title">'
    '🤖 AI Customer Service Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Ask questions, attach files, and get answers '
    'grounded in trusted information.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# ATTACHED FILES
# ============================================================

conversation_files = (
    list_conversation_files(
        current_chat["id"]
    )
)


if conversation_files:

    file_count = len(
        conversation_files
    )

    file_label = (
        "file"
        if file_count == 1
        else "files"
    )

    st.markdown(
        f'<div class="chat-context">'
        f'<strong>📎 {file_count} '
        f'{file_label} attached</strong><br>'
        f'<span>'
        f'Ask about the files directly — '
        f'for example: '
        f'“What is the code related to?”'
        f'</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.expander(
        f"📎 Attached files · {file_count}"
    ):

        for record in conversation_files:

            file_id = record.get(
                "id"
            )

            name = (
                record.get(
                    "original_name"
                )
                or record.get(
                    "file_name"
                )
                or "Attached file"
            )

            size_bytes = record.get(
                "size_bytes",
                0,
            )

            chunk_count = record.get(
                "chunk_count",
                0,
            )

            size_display = (
                record.get(
                    "size_display"
                )
            )

            if not size_display:

                try:

                    if size_bytes < 1024:

                        size_display = (
                            f"{size_bytes} B"
                        )

                    elif size_bytes < (
                        1024 * 1024
                    ):

                        size_display = (
                            f"{size_bytes / 1024:.1f} KB"
                        )

                    else:

                        size_display = (
                            f"{size_bytes / (1024 * 1024):.1f} MB"
                        )

                except (
                    TypeError,
                    ValueError,
                ):

                    size_display = (
                        "Unknown size"
                    )

            column1, column2 = st.columns(
                [5, 1]
            )

            with column1:

                st.markdown(
                    f"**📄 {name}**"
                )

                st.caption(
                    f"{size_display} · "
                    f"{chunk_count} chunks"
                )

            with column2:

                if st.button(
                    "Remove",
                    key=(
                        "remove_file_"
                        + str(file_id)
                    ),
                    use_container_width=True,
                ):

                    success = (
                        remove_conversation_file(
                            current_chat["id"],
                            file_id,
                        )
                    )

                    if success:

                        st.rerun()

                    else:

                        st.error(
                            "Could not remove the file."
                        )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not current_chat.get(
    "messages"
):

    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-icon">💬</div>'
        '<div class="welcome-title">'
        'How can I help you?'
        '</div>'
        '<div class="welcome-text">'
        'Ask a question or attach a PDF, DOCX, TXT '
        'or CSV and ask about its contents.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 💡 Try asking"
    )

    suggestions = [
        "What information is available?",
        "How can I solve a common issue?",
        "What is the code related to?",
        "What does this document contain?",
    ]

    suggestion_columns = st.columns(
        2
    )

    for index, suggestion in enumerate(
        suggestions
    ):

        with suggestion_columns[
            index % 2
        ]:

            if st.button(
                suggestion,
                key=(
                    "suggestion_"
                    + str(index)
                ),
                use_container_width=True,
            ):

                st.session_state.pending_question = (
                    suggestion
                )

                st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for index, message in enumerate(
    current_chat.get(
        "messages",
        [],
    )
):

    role = message.get(
        "role",
        "assistant",
    )

    content = str(
        message.get(
            "content",
            "",
        )
    )

    with st.chat_message(
        role
    ):

        if (
            role == "user"
            and st.session_state.editing_index
            == index
        ):

            edited_text = st.text_area(
                "Edit message",
                value=content,
                key=(
                    "edit_text_"
                    + str(index)
                ),
                height=110,
            )

            save_column, cancel_column = (
                st.columns(2)
            )

            with save_column:

                if st.button(
                    "Save & Regenerate",
                    key=(
                        "save_edit_"
                        + str(index)
                    ),
                    type="primary",
                    use_container_width=True,
                ):

                    edited_text = (
                        edited_text.strip()
                    )

                    if not edited_text:

                        st.warning(
                            "The message cannot be empty."
                        )

                    else:

                        truncate_chat(
                            current_chat,
                            index,
                        )

                        st.session_state.editing_index = (
                            None
                        )

                        st.session_state.pending_question = (
                            edited_text
                        )

                        st.rerun()

            with cancel_column:

                if st.button(
                    "Cancel",
                    key=(
                        "cancel_edit_"
                        + str(index)
                    ),
                    use_container_width=True,
                ):

                    st.session_state.editing_index = (
                        None
                    )

                    st.rerun()

        else:

            st.markdown(
                content
            )

            if role == "assistant":

                render_sources(
                    message.get(
                        "sources",
                        [],
                    )
                )

                feedback = message.get(
                    "feedback"
                )

                action_columns = st.columns(
                    [
                        1,
                        1,
                        1,
                        2,
                        2,
                    ]
                )

                with action_columns[0]:

                    if st.button(
                        "👍",
                        key=(
                            "positive_"
                            + str(index)
                        ),
                        use_container_width=True,
                    ):

                        update_message_feedback(
                            current_chat,
                            index,
                            "positive",
                        )

                        st.rerun()

                with action_columns[1]:

                    if st.button(
                        "👎",
                        key=(
                            "negative_"
                            + str(index)
                        ),
                        use_container_width=True,
                    ):

                        update_message_feedback(
                            current_chat,
                            index,
                            "negative",
                        )

                        st.rerun()

                with action_columns[2]:

                    if st.button(
                        "📋",
                        key=(
                            "copy_"
                            + str(index)
                        ),
                        use_container_width=True,
                    ):

                        st.session_state[
                            "show_copy_"
                            + str(index)
                        ] = True

                        st.rerun()

                with action_columns[3]:

                    if feedback == "positive":

                        st.caption(
                            "👍 Helpful"
                        )

                    elif feedback == "negative":

                        st.caption(
                            "👎 Feedback recorded"
                        )

                with action_columns[4]:

                    response_time = message.get(
                        "response_time"
                    )

                    if response_time is not None:

                        try:

                            st.caption(
                                f"{float(response_time):.2f}s"
                            )

                        except (
                            TypeError,
                            ValueError,
                        ):

                            pass

                if st.session_state.get(
                    "show_copy_"
                    + str(index),
                    False,
                ):

                    st.code(
                        content,
                        language=None,
                    )

                regenerate_column, edit_column = (
                    st.columns(2)
                )

                with regenerate_column:

                    if st.button(
                        "🔄 Regenerate",
                        key=(
                            "regenerate_"
                            + str(index)
                        ),
                        use_container_width=True,
                    ):

                        if (
                            index > 0
                            and current_chat[
                                "messages"
                            ][
                                index - 1
                            ].get(
                                "role"
                            )
                            == "user"
                        ):

                            previous_question = (
                                current_chat[
                                    "messages"
                                ][
                                    index - 1
                                ].get(
                                    "content",
                                    "",
                                )
                            )

                            truncate_chat(
                                current_chat,
                                index,
                            )

                            st.session_state.pending_question = (
                                previous_question
                            )

                            st.rerun()

                with edit_column:

                    if st.button(
                        "✏️ Edit previous",
                        key=(
                            "edit_previous_"
                            + str(index)
                        ),
                        use_container_width=True,
                    ):

                        if (
                            index > 0
                            and current_chat[
                                "messages"
                            ][
                                index - 1
                            ].get(
                                "role"
                            )
                            == "user"
                        ):

                            st.session_state.editing_index = (
                                index - 1
                            )

                            st.rerun()


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_files = st.file_uploader(
    "Attach files to this conversation",
    type=[
        "pdf",
        "docx",
        "txt",
        "csv",
    ],
    accept_multiple_files=True,
    label_visibility="collapsed",
    help=(
        "Files are automatically processed "
        "and indexed for this conversation."
    ),
)


if uploaded_files:

    upload_signature_parts = []

    for uploaded_file in uploaded_files:

        try:

            file_bytes = (
                uploaded_file.getvalue()
            )

            upload_signature_parts.append(
                (
                    uploaded_file.name,
                    len(file_bytes),
                )
            )

        except Exception:

            upload_signature_parts.append(
                (
                    uploaded_file.name,
                    0,
                )
            )

    upload_signature = "|".join(
        sorted(
            f"{name}:{size}"
            for name, size
            in upload_signature_parts
        )
    )

    current_signature = (
        str(
            st.session_state.get(
                "upload_signature",
                "",
            )
        )
    )

    if (
        upload_signature
        != current_signature
    ):

        result = add_conversation_files(
            current_chat["id"],
            uploaded_files,
        )

        st.session_state.upload_signature = (
            upload_signature
        )

        errors = result.get(
            "errors",
            [],
        )

        skipped = result.get(
            "skipped",
            [],
        )

        added = result.get(
            "added",
            [],
        )

        for error in errors:

            st.error(
                str(error)
            )

        if added:

            st.success(
                f"Added {len(added)} file(s) "
                "to this conversation."
            )

            st.rerun()

        elif skipped and not errors:

            st.session_state.upload_signature = (
                upload_signature
            )


# ============================================================
# PENDING QUESTION
# ============================================================

if st.session_state.pending_question:

    pending_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = (
        None
    )

    process_question(
        pending_question
    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Message AI Support..."
)

if question:

    process_question(
        question
    )