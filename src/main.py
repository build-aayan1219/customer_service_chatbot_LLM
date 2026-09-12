import html
import inspect
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
    save_chat,
    search_chats,
    set_chat_archived,
    set_chat_pinned,
    truncate_chat,
    update_message_feedback,
)

from src.conversation_files import (
    add_conversation_files,
    delete_all_conversation_files,
    get_attachment_signature,
    list_conversation_files,
    remove_conversation_file,
)

from src.langchain_helper import get_qa_stream


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PRODUCT UI
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #ffffff;
}

[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.94);
}

[data-testid="stSidebar"] {
    background: #f7f7f8;
    border-right: 1px solid #e5e5e5;
}

[data-testid="stSidebarContent"] {
    padding: 12px 10px 72px;
}

.block-container {
    max-width: 900px;
    padding-top: 12px;
    padding-bottom: 100px;
}


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

.brand {
    padding: 7px 7px 12px;
}

.brand-title {
    font-size: 18px;
    font-weight: 750;
}

.brand-sub {
    color: #777777;
    font-size: 11px;
    margin-top: 2px;
}

.profile {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 265px;
    padding: 9px 12px;
    background: #f7f7f8;
    border-top: 1px solid #e5e5e5;
}

.profile-name {
    font-size: 12px;
    font-weight: 650;
}

.profile-plan {
    font-size: 10px;
    color: #777777;
}


/* ----------------------------------------------------------
   TOP BAR
---------------------------------------------------------- */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #eeeeee;
    padding: 4px 0 12px;
    margin-bottom: 18px;
}

.top-title {
    font-size: 16px;
    font-weight: 700;
}

.top-subtitle {
    color: #777777;
    font-size: 11px;
    margin-top: 2px;
}


/* ----------------------------------------------------------
   WELCOME
---------------------------------------------------------- */

.welcome {
    text-align: center;
    padding: 110px 0 28px;
}

.welcome-icon {
    font-size: 34px;
}

.welcome-title {
    font-size: 29px;
    font-weight: 720;
    letter-spacing: -1px;
    margin-top: 8px;
}

.welcome-sub {
    color: #777777;
    font-size: 13px;
    margin-top: 7px;
}

.suggest-title {
    color: #777777;
    font-size: 12px;
    font-weight: 650;
    margin: 12px 0 7px;
}


/* ----------------------------------------------------------
   FILE CONTEXT
---------------------------------------------------------- */

.context {
    border: 1px solid #e5e5e5;
    background: #f7f7f8;
    border-radius: 11px;
    padding: 9px 12px;
    margin-bottom: 10px;
}

.context-title {
    font-size: 12px;
    font-weight: 650;
}

.context-sub {
    color: #777777;
    font-size: 10px;
    margin-top: 2px;
}


/* ----------------------------------------------------------
   SOURCES
---------------------------------------------------------- */

.source-group {
    border: 1px solid #e5e5e5;
    background: #f7f7f8;
    border-radius: 10px;
    padding: 8px 10px;
    margin: 5px 0;
}

.source-name {
    font-size: 12px;
    font-weight: 650;
}

.source-meta {
    color: #777777;
    font-size: 10px;
    margin-top: 2px;
}


/* ----------------------------------------------------------
   COMPOSER
---------------------------------------------------------- */

.note {
    color: #888888;
    font-size: 10px;
    text-align: center;
    margin: 3px 0 7px;
}


/* ----------------------------------------------------------
   DASHBOARD
---------------------------------------------------------- */

.dashboard-title {
    font-size: 25px;
    font-weight: 750;
    letter-spacing: -0.5px;
}

.dashboard-subtitle {
    color: #777777;
    font-size: 12px;
    margin-bottom: 20px;
}

.metric {
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 12px;
    background: #fafafa;
}

.metric-label {
    color: #777777;
    font-size: 10px;
}

.metric-value {
    font-size: 22px;
    font-weight: 700;
    margin-top: 3px;
}


/* ----------------------------------------------------------
   BUTTON REFINEMENT
---------------------------------------------------------- */

button[kind="secondary"],
button[kind="tertiary"] {
    border-radius: 10px !important;
}

button[kind="primary"] {
    border-radius: 10px !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_chat_id" not in st.session_state:

    chats = load_chats()

    if chats:

        st.session_state.current_chat_id = (
            chats[0]["id"]
        )

    else:

        chat = create_chat()

        save_chat(
            chat
        )

        st.session_state.current_chat_id = (
            chat["id"]
        )


if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False


if "search_text" not in st.session_state:
    st.session_state.search_text = ""


if "editing_index" not in st.session_state:
    st.session_state.editing_index = None


if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


if "attachment_signature" not in st.session_state:
    st.session_state.attachment_signature = ""


if "show_sources" not in st.session_state:
    st.session_state.show_sources = True


# ============================================================
# CHAT HELPERS
# ============================================================

def get_current_chat():

    chats = load_chats()

    chat = find_chat(
        chats,
        st.session_state.current_chat_id,
    )

    if chat is None:

        chat = create_chat()

        save_chat(
            chat
        )

        st.session_state.current_chat_id = (
            chat["id"]
        )

    return chat


def start_new_chat():

    chat = create_chat()

    save_chat(
        chat
    )

    st.session_state.current_chat_id = (
        chat["id"]
    )

    st.session_state.show_dashboard = False
    st.session_state.editing_index = None
    st.session_state.pending_question = None
    st.session_state.attachment_signature = ""

    st.rerun()


# ============================================================
# SOURCE HELPERS
# ============================================================

def get_source_data(source):

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


def get_source_key(metadata):

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

    if not st.session_state.show_sources:
        return

    groups = defaultdict(list)

    for source in sources:

        content, metadata = (
            get_source_data(
                source
            )
        )

        groups[
            get_source_key(
                metadata
            )
        ].append(
            (
                content,
                metadata,
            )
        )

    total_groups = len(
        groups
    )

    source_label = (
        "source"
        if total_groups == 1
        else "sources"
    )

    with st.expander(
        f"📚 {total_groups} {source_label}"
    ):

        for (
            group_key,
            items,
        ) in groups.items():

            kind, name = (
                group_key
            )

            if kind == "file":

                icon = "📄"
                origin = "Conversation file"

            else:

                icon = "📚"
                origin = "Knowledge Base"

            section_label = (
                "section"
                if len(items) == 1
                else "sections"
            )

            st.markdown(
                f'<div class="source-group">'
                f'<div class="source-name">'
                f'{icon} '
                f'{html.escape(str(name))}'
                f'</div>'
                f'<div class="source-meta">'
                f'{len(items)} relevant '
                f'{section_label} · '
                f'{origin}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            for number, (
                content,
                metadata,
            ) in enumerate(
                items,
                1,
            ):

                location = (
                    metadata.get(
                        "section"
                    )
                    or metadata.get(
                        "location"
                    )
                    or (
                        f"Relevant section "
                        f"{number}"
                    )
                )

                with st.expander(
                    str(location)
                ):

                    st.write(
                        content
                    )


# ============================================================
# EXPORT
# ============================================================

def export_markdown(chat):

    lines = [
        f"# {chat.get('title', 'Conversation')}",
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
# ANALYTICS
# ============================================================

def calculate_metrics(chats):

    questions = 0
    answers = 0
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

                answers += 1

                feedback = message.get(
                    "feedback"
                )

                if feedback == "positive":

                    positive += 1

                elif feedback == "negative":

                    negative += 1

                response_time = (
                    message.get(
                        "response_time"
                    )
                )

                try:

                    if response_time is not None:

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
        "answers": answers,
        "positive": positive,
        "negative": negative,
        "satisfaction": satisfaction,
        "average": average_time,
    }


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(
    question
):

    question = str(
        question or ""
    ).strip()

    if not question:
        return

    chat = get_current_chat()

    chat_id = chat["id"]

    history = list(
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

    start_time = time.time()

    try:

        stream, sources = (
            get_qa_stream(
                question,
                chat_history=history,
                chat_id=chat_id,
            )
        )

        with st.chat_message(
            "assistant"
        ):

            answer = st.write_stream(
                stream
            )

        if not isinstance(
            answer,
            str,
        ):

            answer = "".join(
                str(part)
                for part in answer
            )

        answer = answer.strip()

        elapsed = (
            time.time()
            - start_time
        )

        refreshed_chat = find_chat(
            load_chats(),
            chat_id,
        )

        if refreshed_chat is None:

            st.error(
                "The conversation could not be saved."
            )

            return

        add_message(
            refreshed_chat,
            "assistant",
            answer,
            sources=sources,
            response_time=elapsed,
        )

        st.rerun()

    except Exception as error:

        error_text = str(
            error
        )

        lowered = (
            error_text.lower()
        )

        if (
            "429" in lowered
            or "resource_exhausted"
            in lowered
            or "quota" in lowered
        ):

            st.error(
                "⚠️ Gemini is temporarily unavailable because the API usage limit was reached."
            )

        else:

            st.error(
                "⚠️ Something went wrong while generating the response."
            )

            st.caption(
                error_text
            )


# ============================================================
# CURRENT CHAT
# ============================================================

chat = get_current_chat()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">'
        '<div class="brand-title">'
        '🤖 AI Support'
        '</div>'
        '<div class="brand-sub">'
        'Intelligent customer service assistant'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New chat",
        use_container_width=True,
        type="primary",
    ):

        start_new_chat()

    search = st.text_input(
        "Search",
        value=st.session_state.search_text,
        placeholder="Search chats...",
        label_visibility="collapsed",
    )

    st.session_state.search_text = (
        search
    )

    chats = load_chats()

    if search.strip():

        visible_chats = (
            search_chats(
                chats,
                search,
            )
        )

    else:

        visible_chats = chats

    pinned_chats = [
        item
        for item in visible_chats
        if item.get(
            "pinned",
            False,
        )
    ]

    regular_chats = [
        item
        for item in visible_chats
        if (
            not item.get(
                "pinned",
                False,
            )
            and not item.get(
                "archived",
                False,
            )
        )
    ]

    archived_chats = [
        item
        for item in visible_chats
        if item.get(
            "archived",
            False,
        )
    ]

    if pinned_chats:

        st.caption(
            "PINNED"
        )

        for item in pinned_chats:

            title = str(
                item.get(
                    "title",
                    "New Chat",
                )
            )

            if len(title) > 31:

                title = (
                    title[:28]
                    + "..."
                )

            if st.button(
                "📌 " + title,
                key=(
                    "pinned_"
                    + item["id"]
                ),
                use_container_width=True,
            ):

                st.session_state.current_chat_id = (
                    item["id"]
                )

                st.session_state.show_dashboard = (
                    False
                )

                st.rerun()

    st.caption(
        "CHATS"
    )

    if not regular_chats:

        st.caption(
            "No conversations yet"
        )

    for item in regular_chats:

        title = str(
            item.get(
                "title",
                "New Chat",
            )
        )

        if len(title) > 31:

            title = (
                title[:28]
                + "..."
            )

        if (
            item["id"]
            == st.session_state.current_chat_id
        ):

            prefix = "● "

        else:

            prefix = ""

        if st.button(
            prefix + title,
            key=(
                "chat_"
                + item["id"]
            ),
            use_container_width=True,
        ):

            st.session_state.current_chat_id = (
                item["id"]
            )

            st.session_state.show_dashboard = (
                False
            )

            st.session_state.editing_index = (
                None
            )

            st.rerun()

    if archived_chats:

        with st.expander(
            f"Archived · {len(archived_chats)}"
        ):

            for item in archived_chats:

                title = str(
                    item.get(
                        "title",
                        "New Chat",
                    )
                )

                if len(title) > 31:

                    title = (
                        title[:28]
                        + "..."
                    )

                if st.button(
                    "🗃️ " + title,
                    key=(
                        "archived_"
                        + item["id"]
                    ),
                    use_container_width=True,
                ):

                    st.session_state.current_chat_id = (
                        item["id"]
                    )

                    st.session_state.show_dashboard = (
                        False
                    )

                    st.rerun()

    st.markdown(
        '<div class="profile">'
        '<div class="profile-name">'
        'AS&nbsp;&nbsp; Aayan Shaikh'
        '</div>'
        '<div class="profile-plan">'
        'Free plan'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# TOP HEADER
# ============================================================

left_column, right_column = (
    st.columns(
        [8, 1]
    )
)

with left_column:

    title = html.escape(
        str(
            chat.get(
                "title",
                "New Chat",
            )
        )
    )

    st.markdown(
        f'<div class="topbar">'
        f'<div>'
        f'<div class="top-title">'
        f'{title}'
        f'</div>'
        f'<div class="top-subtitle">'
        f'Gemini 3.6 Flash · '
        f'Retrieval-Augmented Generation'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


with right_column:

    if hasattr(
        st,
        "popover",
    ):

        settings_menu = st.popover(
            "•••",
            use_container_width=True,
        )

    else:

        settings_menu = st.expander(
            "•••",
            expanded=False,
        )

    with settings_menu:

        st.markdown(
            "**Settings**"
        )

        st.session_state.show_sources = (
            st.toggle(
                "Show sources",
                value=st.session_state.show_sources,
            )
        )

        st.caption(
            "Model"
        )

        st.selectbox(
            "Model",
            [
                "Gemini 3.6 Flash"
            ],
            label_visibility="collapsed",
        )

        st.divider()

        if st.button(
            "📊 Analytics",
            use_container_width=True,
            key="open_analytics",
        ):

            st.session_state.show_dashboard = (
                True
            )

            st.rerun()

        st.download_button(
            "⬇️ Export conversation",
            data=export_markdown(
                chat
            ),
            file_name="conversation.md",
            mime="text/markdown",
            use_container_width=True,
        )

        st.divider()

        rename_value = st.text_input(
            "Conversation name",
            value=chat.get(
                "title",
                "New Chat",
            ),
            key="settings_title",
        )

        if st.button(
            "Save name",
            use_container_width=True,
            key="save_name",
        ):

            rename_chat(
                chat,
                rename_value,
            )

            st.rerun()

        if st.button(
            "📌 "
            + (
                "Unpin conversation"
                if chat.get(
                    "pinned",
                    False,
                )
                else
                "Pin conversation"
            ),
            use_container_width=True,
            key="pin_conversation",
        ):

            set_chat_pinned(
                chat,
                not chat.get(
                    "pinned",
                    False,
                ),
            )

            st.rerun()

        if st.button(
            "🗃️ "
            + (
                "Unarchive conversation"
                if chat.get(
                    "archived",
                    False,
                )
                else
                "Archive conversation"
            ),
            use_container_width=True,
            key="archive_conversation",
        ):

            set_chat_archived(
                chat,
                not chat.get(
                    "archived",
                    False,
                ),
            )

            st.rerun()

        if st.button(
            "🗑️ Delete conversation",
            use_container_width=True,
            key="delete_conversation",
        ):

            chat_id = chat["id"]

            remaining = delete_chat(
                load_chats(),
                chat_id,
            )

            delete_all_conversation_files(
                [
                    chat_id
                ]
            )

            if remaining:

                st.session_state.current_chat_id = (
                    remaining[0]["id"]
                )

            else:

                replacement = create_chat()

                save_chat(
                    replacement
                )

                st.session_state.current_chat_id = (
                    replacement["id"]
                )

            st.session_state.editing_index = (
                None
            )

            st.rerun()

        if st.button(
            "🧹 Delete all conversations",
            use_container_width=True,
            key="delete_all_conversations",
        ):

            ids = [
                item["id"]
                for item in load_chats()
            ]

            delete_all_chats()

            if ids:

                delete_all_conversation_files(
                    ids
                )

            replacement = create_chat()

            save_chat(
                replacement
            )

            st.session_state.current_chat_id = (
                replacement["id"]
            )

            st.session_state.editing_index = (
                None
            )

            st.rerun()

        st.divider()

        st.caption(
            "AI Support"
        )

        st.caption(
            "Gemini + LangChain + FAISS + RAG"
        )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.show_dashboard:

    dashboard_data = (
        calculate_metrics(
            load_chats()
        )
    )

    st.markdown(
        '<div class="dashboard-title">'
        'Analytics'
        '</div>'
        '<div class="dashboard-subtitle">'
        'Conversation activity and response performance'
        '</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(
        4
    )

    metric_values = [
        (
            "Chats",
            dashboard_data["chats"],
        ),
        (
            "Questions",
            dashboard_data["questions"],
        ),
        (
            "AI responses",
            dashboard_data["answers"],
        ),
        (
            "Avg response",
            f'{dashboard_data["average"]:.2f}s',
        ),
    ]

    for column, (
        label,
        value,
    ) in zip(
        columns,
        metric_values,
    ):

        with column:

            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-label">'
                f'{label}'
                f'</div>'
                f'<div class="metric-value">'
                f'{value}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    feedback_columns = st.columns(
        3
    )

    feedback_values = [
        (
            "Positive feedback",
            dashboard_data["positive"],
        ),
        (
            "Negative feedback",
            dashboard_data["negative"],
        ),
        (
            "Satisfaction",
            f'{dashboard_data["satisfaction"]:.0f}%',
        ),
    ]

    for column, (
        label,
        value,
    ) in zip(
        feedback_columns,
        feedback_values,
    ):

        with column:

            st.metric(
                label,
                value,
            )

    st.divider()

    if st.button(
        "← Back to chat",
        use_container_width=True,
    ):

        st.session_state.show_dashboard = (
            False
        )

        st.rerun()

    st.stop()


# ============================================================
# ATTACHED FILES
# ============================================================

attached_files = (
    list_conversation_files(
        chat["id"]
    )
)

if attached_files:

    file_count = len(
        attached_files
    )

    file_label = (
        "file"
        if file_count == 1
        else "files"
    )

    st.markdown(
        f'<div class="context">'
        f'<div class="context-title">'
        f'📎 {file_count} {file_label} attached'
        f'</div>'
        f'<div class="context-sub">'
        f'These files are available to the assistant '
        f'in this conversation.'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.expander(
        "View attachments"
    ):

        for record in attached_files:

            file_id = record.get(
                "id"
            )

            file_name = (
                record.get(
                    "original_name"
                )
                or record.get(
                    "file_name"
                )
                or "Attached file"
            )

            size_display = record.get(
                "size_display",
                "",
            )

            chunk_count = record.get(
                "chunk_count",
                0,
            )

            file_column, remove_column = (
                st.columns(
                    [8, 1]
                )
            )

            with file_column:

                st.markdown(
                    f"**📄 {file_name}**"
                )

                st.caption(
                    f"{size_display} · "
                    f"{chunk_count} indexed chunks"
                )

            with remove_column:

                if st.button(
                    "×",
                    key=(
                        "remove_"
                        + str(file_id)
                    ),
                    help="Remove file",
                ):

                    removed = (
                        remove_conversation_file(
                            chat["id"],
                            file_id,
                        )
                    )

                    if removed:

                        st.session_state.attachment_signature = (
                            ""
                        )

                        st.rerun()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not chat.get(
    "messages"
):

    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-icon">✦</div>'
        '<div class="welcome-title">'
        'How can I help you?'
        '</div>'
        '<div class="welcome-sub">'
        'Ask a question, or attach a file and '
        'ask about its contents.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="suggest-title">'
        'Try asking'
        '</div>',
        unsafe_allow_html=True,
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
# CHAT MESSAGES
# ============================================================

for index, message in enumerate(
    chat.get(
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

            edited_message = st.text_area(
                "Edit message",
                value=content,
                key=(
                    "edit_box_"
                    + str(index)
                ),
                label_visibility="collapsed",
                height=100,
            )

            save_column, cancel_column = (
                st.columns(
                    2
                )
            )

            with save_column:

                if st.button(
                    "Save & regenerate",
                    key=(
                        "save_edit_"
                        + str(index)
                    ),
                    type="primary",
                    use_container_width=True,
                ):

                    edited_message = (
                        edited_message.strip()
                    )

                    if edited_message:

                        truncate_chat(
                            chat,
                            index,
                        )

                        st.session_state.editing_index = (
                            None
                        )

                        st.session_state.pending_question = (
                            edited_message
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Message cannot be empty."
                        )

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

                action_a, action_b, action_c, action_d, action_e = (
                    st.columns(
                        [
                            1,
                            1,
                            1,
                            1,
                            7,
                        ]
                    )
                )

                with action_a:

                    if st.button(
                        "👍",
                        key=(
                            "like_"
                            + str(index)
                        ),
                        help="Good response",
                    ):

                        update_message_feedback(
                            chat,
                            index,
                            "positive",
                        )

                        st.rerun()

                with action_b:

                    if st.button(
                        "👎",
                        key=(
                            "dislike_"
                            + str(index)
                        ),
                        help="Needs improvement",
                    ):

                        update_message_feedback(
                            chat,
                            index,
                            "negative",
                        )

                        st.rerun()

                with action_c:

                    if st.button(
                        "↻",
                        key=(
                            "regenerate_"
                            + str(index)
                        ),
                        help="Regenerate response",
                    ):

                        if (
                            index > 0
                            and chat[
                                "messages"
                            ][
                                index - 1
                            ].get(
                                "role"
                            )
                            == "user"
                        ):

                            previous_question = (
                                chat[
                                    "messages"
                                ][
                                    index - 1
                                ].get(
                                    "content",
                                    "",
                                )
                            )

                            truncate_chat(
                                chat,
                                index,
                            )

                            st.session_state.pending_question = (
                                previous_question
                            )

                            st.rerun()

                with action_d:

                    if st.button(
                        "✎",
                        key=(
                            "edit_previous_"
                            + str(index)
                        ),
                        help="Edit previous message",
                    ):

                        if (
                            index > 0
                            and chat[
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

                with action_e:

                    response_time = (
                        message.get(
                            "response_time"
                        )
                    )

                    try:

                        if response_time is not None:

                            st.caption(
                                f"{float(response_time):.2f}s"
                            )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass


# ============================================================
# FILE ATTACHMENT SUPPORT
# ============================================================

chat_input_parameters = (
    inspect.signature(
        st.chat_input
    ).parameters
)

chat_input_supports_files = (
    "accept_file"
    in chat_input_parameters
)

uploaded_files = []


# ============================================================
# OLD STREAMLIT FALLBACK
# ============================================================

if not chat_input_supports_files:

    st.markdown(
        '<div class="note">'
        'Use Attach to add PDF, DOCX, TXT or CSV files.'
        '</div>',
        unsafe_allow_html=True,
    )

    if hasattr(
        st,
        "popover",
    ):

        attachment_menu = st.popover(
            "＋ Attach",
            use_container_width=False,
        )

    else:

        attachment_menu = st.expander(
            "＋ Attach",
            expanded=False,
        )

    with attachment_menu:

        uploaded_files = st.file_uploader(
            "Attach files",
            type=[
                "pdf",
                "docx",
                "txt",
                "csv",
            ],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="fallback_file_uploader",
        )


# ============================================================
# PROCESS UPLOADED FILES
# ============================================================

if uploaded_files:

    signature = (
        get_attachment_signature(
            uploaded_files
        )
    )

    if (
        signature
        != st.session_state.attachment_signature
    ):

        result = (
            add_conversation_files(
                chat["id"],
                uploaded_files,
            )
        )

        st.session_state.attachment_signature = (
            signature
        )

        for error in result.get(
            "errors",
            [],
        ):

            st.error(
                str(error)
            )

        added_files = result.get(
            "added",
            [],
        )

        if added_files:

            st.success(
                f"Added {len(added_files)} file(s)."
            )

            st.rerun()


# ============================================================
# PENDING QUESTIONS
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
# CHAT COMPOSER
# ============================================================

if chat_input_supports_files:

    chat_value = st.chat_input(
        "Message AI Support...",
        accept_file=True,
        file_type=[
            "pdf",
            "docx",
            "txt",
            "csv",
        ],
    )

    if chat_value:

        question_text = getattr(
            chat_value,
            "text",
            "",
        )

        files_from_chat = getattr(
            chat_value,
            "files",
            [],
        )

        if files_from_chat:

            signature = (
                get_attachment_signature(
                    files_from_chat
                )
            )

            if (
                signature
                != st.session_state.attachment_signature
            ):

                result = (
                    add_conversation_files(
                        chat["id"],
                        files_from_chat,
                    )
                )

                st.session_state.attachment_signature = (
                    signature
                )

                for error in result.get(
                    "errors",
                    [],
                ):

                    st.error(
                        str(error)
                    )

        if (
            question_text
            and str(
                question_text
            ).strip()
        ):

            process_question(
                str(
                    question_text
                ).strip()
            )

else:

    question = st.chat_input(
        "Message AI Support..."
    )

    if question:

        process_question(
            question
        )