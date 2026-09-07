import json
import sqlite3
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "chat_history.db"

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "dataset.csv"
)

VECTORDB_PATH = (
    BASE_DIR / "faiss_index"
)

UNKNOWN_RESPONSE = (
    "I don't know based on the available information."
)


def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


def load_chats():

    if not DATABASE_PATH.exists():
        return []

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT
                id,
                title,
                messages,
                created_at,
                updated_at
            FROM chats
            ORDER BY updated_at DESC
            """
        ).fetchall()

    except sqlite3.Error:

        connection.close()

        return []

    connection.close()

    chats = []

    for row in rows:

        try:

            messages = json.loads(
                row["messages"]
            )

        except (
            json.JSONDecodeError,
            TypeError,
        ):

            messages = []

        chats.append(
            {
                "id": row["id"],
                "title": row["title"],
                "messages": messages,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )

    return chats


def calculate_analytics(chats):

    total_conversations = len(chats)

    total_questions = 0
    total_responses = 0

    unknown_queries = 0

    positive_feedback = 0
    negative_feedback = 0

    questions = []

    response_times = []

    daily_activity = Counter()

    for chat in chats:

        updated_at = chat.get(
            "updated_at",
            "",
        )

        if updated_at:

            date = str(
                updated_at
            ).split(" ")[0]

            daily_activity[date] += 1

        for message in chat.get(
            "messages",
            [],
        ):

            role = message.get(
                "role",
                "",
            )

            content = str(
                message.get(
                    "content",
                    "",
                )
            ).strip()

            if role == "user":

                total_questions += 1

                if content:

                    questions.append(
                        content
                    )

            elif role == "assistant":

                total_responses += 1

                if content == UNKNOWN_RESPONSE:

                    unknown_queries += 1

                feedback = message.get(
                    "feedback"
                )

                if feedback == "positive":

                    positive_feedback += 1

                elif feedback == "negative":

                    negative_feedback += 1

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

    popular_questions = Counter(
        question.strip()
        for question in questions
        if question.strip()
    )

    if response_times:

        average_response_time = (
            sum(response_times)
            / len(response_times)
        )

        fastest_response = min(
            response_times
        )

        slowest_response = max(
            response_times
        )

    else:

        average_response_time = None
        fastest_response = None
        slowest_response = None

    total_feedback = (
        positive_feedback
        + negative_feedback
    )

    if total_feedback:

        satisfaction_rate = (
            positive_feedback
            / total_feedback
        ) * 100

    else:

        satisfaction_rate = None

    if total_responses:

        unknown_rate = (
            unknown_queries
            / total_responses
        ) * 100

    else:

        unknown_rate = 0

    return {
        "total_conversations":
            total_conversations,

        "total_questions":
            total_questions,

        "total_responses":
            total_responses,

        "unknown_queries":
            unknown_queries,

        "positive_feedback":
            positive_feedback,

        "negative_feedback":
            negative_feedback,

        "satisfaction_rate":
            satisfaction_rate,

        "unknown_rate":
            unknown_rate,

        "average_response_time":
            average_response_time,

        "fastest_response":
            fastest_response,

        "slowest_response":
            slowest_response,

        "popular_questions":
            popular_questions,

        "daily_activity":
            daily_activity,
    }


def get_knowledge_base_stats():

    rows = 0
    columns = 0
    file_size = 0
    last_updated = "Unavailable"

    if DATASET_PATH.exists():

        try:

            dataframe = pd.read_csv(
                DATASET_PATH
            )

            rows = len(dataframe)

            columns = len(
                dataframe.columns
            )

            file_size = (
                DATASET_PATH.stat().st_size
                / 1024
            )

            last_updated = (
                pd.to_datetime(
                    DATASET_PATH.stat().st_mtime,
                    unit="s",
                ).strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

        except Exception:

            pass

    return {
        "dataset_rows": rows,
        "dataset_columns": columns,
        "file_size_kb": file_size,
        "last_updated": last_updated,
        "vector_db_available":
            VECTORDB_PATH.exists(),
    }


def metric_card(
    label,
    value,
):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analytics():

    st.markdown(
        """
        <style>

        .dashboard-title {
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .dashboard-subtitle {
            color: #777;
            margin-bottom: 25px;
        }

        .metric-card {
            padding: 20px;
            border-radius: 14px;
            border: 1px solid
                rgba(128,128,128,0.25);
            background:
                rgba(128,128,128,0.06);
            min-height: 125px;
        }

        .metric-label {
            font-size: 14px;
            color: #777;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 30px;
            font-weight: 700;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 650;
            margin-top: 30px;
            margin-bottom: 15px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    chats = load_chats()

    analytics = calculate_analytics(
        chats
    )

    knowledge_base = (
        get_knowledge_base_stats()
    )

    st.markdown(
        '<div class="dashboard-title">'
        '📊 Analytics Dashboard'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="dashboard-subtitle">
            Monitor chatbot usage, performance,
            customer satisfaction and
            knowledge-base activity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🔄 Refresh Analytics"
    ):

        st.rerun()

    st.markdown(
        '<div class="section-title">'
        'Overview'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(
            "Total Conversations",
            analytics[
                "total_conversations"
            ],
        )

    with col2:

        metric_card(
            "Total Questions",
            analytics[
                "total_questions"
            ],
        )

    with col3:

        metric_card(
            "AI Responses",
            analytics[
                "total_responses"
            ],
        )

    with col4:

        metric_card(
            "Knowledge Base Entries",
            knowledge_base[
                "dataset_rows"
            ],
        )

    st.markdown(
        '<div class="section-title">'
        '⚡ Performance'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    average = analytics[
        "average_response_time"
    ]

    fastest = analytics[
        "fastest_response"
    ]

    slowest = analytics[
        "slowest_response"
    ]

    with col1:

        st.metric(
            "Average Response Time",
            f"{average:.2f}s"
            if average is not None
            else "No data",
        )

    with col2:

        st.metric(
            "Fastest Response",
            f"{fastest:.2f}s"
            if fastest is not None
            else "No data",
        )

    with col3:

        st.metric(
            "Slowest Response",
            f"{slowest:.2f}s"
            if slowest is not None
            else "No data",
        )

    with col4:

        st.metric(
            "Unknown Queries",
            analytics[
                "unknown_queries"
            ],
        )

    st.markdown(
        '<div class="section-title">'
        '🎯 Response Quality'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Unknown Rate",
            f'{analytics["unknown_rate"]:.1f}%',
        )

    with col2:

        satisfaction = analytics[
            "satisfaction_rate"
        ]

        st.metric(
            "Satisfaction",
            f"{satisfaction:.1f}%"
            if satisfaction is not None
            else "No feedback",
        )

    with col3:

        st.metric(
            "👍 Positive",
            analytics[
                "positive_feedback"
            ],
        )

    with col4:

        st.metric(
            "👎 Negative",
            analytics[
                "negative_feedback"
            ],
        )

    st.markdown(
        '<div class="section-title">'
        '🔥 Popular Questions'
        '</div>',
        unsafe_allow_html=True,
    )

    popular_questions = analytics[
        "popular_questions"
    ]

    if popular_questions:

        popular_data = []

        for question, count in (
            popular_questions
            .most_common(10)
        ):

            popular_data.append(
                {
                    "Question": question,
                    "Times Asked": count,
                }
            )

        popular_df = pd.DataFrame(
            popular_data
        )

        st.dataframe(
            popular_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No questions have been asked yet."
        )

    st.markdown(
        '<div class="section-title">'
        '📈 Conversation Activity'
        '</div>',
        unsafe_allow_html=True,
    )

    daily_activity = analytics[
        "daily_activity"
    ]

    if daily_activity:

        activity_data = pd.DataFrame(
            [
                {
                    "Date": date,
                    "Conversations": count,
                }
                for date, count
                in sorted(
                    daily_activity.items()
                )
            ]
        )

        activity_data["Date"] = (
            pd.to_datetime(
                activity_data["Date"]
            )
        )

        activity_data = (
            activity_data
            .set_index("Date")
        )

        st.line_chart(
            activity_data[
                "Conversations"
            ]
        )

    else:

        st.info(
            "Conversation activity will "
            "appear after users start chatting."
        )

    st.markdown(
        '<div class="section-title">'
        '📚 Knowledge Base'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Dataset Entries",
            knowledge_base[
                "dataset_rows"
            ],
        )

    with col2:

        st.metric(
            "Dataset Columns",
            knowledge_base[
                "dataset_columns"
            ],
        )

    with col3:

        st.metric(
            "Dataset Size",
            f'{knowledge_base["file_size_kb"]:.1f} KB',
        )

    with col4:

        if knowledge_base[
            "vector_db_available"
        ]:

            st.success(
                "🟢 Vector DB Ready"
            )

        else:

            st.warning(
                "🟡 Vector DB Not Found"
            )

    st.caption(
        "Last dataset update: "
        + knowledge_base[
            "last_updated"
        ]
    )

    st.markdown(
        '<div class="section-title">'
        '🕒 Recent Conversations'
        '</div>',
        unsafe_allow_html=True,
    )

    if chats:

        recent_data = []

        for chat in chats[:10]:

            recent_data.append(
                {
                    "Title":
                        chat.get(
                            "title",
                            "New Chat",
                        ),

                    "Messages":
                        len(
                            chat.get(
                                "messages",
                                [],
                            )
                        ),

                    "Last Updated":
                        chat.get(
                            "updated_at",
                            "",
                        ),
                }
            )

        recent_df = pd.DataFrame(
            recent_data
        )

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No conversations available."
        )

    st.markdown(
        '<div class="section-title">'
        '🟢 System Status'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if knowledge_base[
            "vector_db_available"
        ]:

            st.success(
                "Knowledge Base: Online"
            )

        else:

            st.warning(
                "Knowledge Base: Offline"
            )

    with col2:

        if DATABASE_PATH.exists():

            st.success(
                "Chat Database: Connected"
            )

        else:

            st.warning(
                "Chat Database: Not Created"
            )

    with col3:

        st.success(
            "Analytics Engine: Active"
        )