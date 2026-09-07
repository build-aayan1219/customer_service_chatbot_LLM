import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "chat_history.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            messages TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def serialize_sources(sources):
    serialized = []

    for source in sources or []:

        if hasattr(source, "page_content"):

            serialized.append(
                {
                    "page_content": source.page_content,
                    "metadata": getattr(
                        source,
                        "metadata",
                        {},
                    ),
                }
            )

        elif isinstance(source, dict):

            serialized.append(
                {
                    "page_content": source.get(
                        "page_content",
                        "",
                    ),
                    "metadata": source.get(
                        "metadata",
                        {},
                    ),
                }
            )

    return serialized


def deserialize_sources(sources):
    return sources or []


def serialize_messages(messages):
    serialized = []

    for message in messages:

        serialized.append(
            {
                "role": message.get(
                    "role",
                    "",
                ),
                "content": message.get(
                    "content",
                    "",
                ),
                "sources": serialize_sources(
                    message.get(
                        "sources",
                        [],
                    )
                ),
                "response_time": message.get(
                    "response_time"
                ),
                "feedback": message.get(
                    "feedback"
                ),
            }
        )

    return serialized


def create_chat():

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": [],
        "created_at": now,
        "updated_at": now,
    }


def create_message(
    role,
    content,
    sources=None,
    response_time=None,
    feedback=None,
):

    return {
        "role": role,
        "content": content,
        "sources": sources or [],
        "response_time": response_time,
        "feedback": feedback,
    }


def generate_chat_title(question):

    question = question.strip()

    if not question:
        return "New Chat"

    words = question.split()

    if len(words) <= 6:
        return question

    return " ".join(words[:6]) + "..."


def add_message(
    chat,
    role,
    content,
    sources=None,
    response_time=None,
    feedback=None,
):

    message = create_message(
        role=role,
        content=content,
        sources=sources,
        response_time=response_time,
        feedback=feedback,
    )

    chat["messages"].append(message)

    chat["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if (
        chat["title"] == "New Chat"
        and role == "user"
    ):
        chat["title"] = generate_chat_title(
            content
        )

    save_chat(chat)

    return message


def find_chat(chats, chat_id):

    for chat in chats:

        if chat["id"] == chat_id:
            return chat

    return None


def rename_chat(chat, new_title):

    new_title = new_title.strip()

    if new_title:
        chat["title"] = new_title

    chat["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    save_chat(chat)

    return chat


def update_chat(chat):

    chat["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    save_chat(chat)

    return chat


def update_message_feedback(
    chat,
    message_index,
    feedback,
):

    allowed_feedback = {
        "positive",
        "negative",
        None,
    }

    if feedback not in allowed_feedback:

        raise ValueError(
            "Invalid feedback value."
        )

    if (
        message_index < 0
        or message_index >= len(
            chat["messages"]
        )
    ):
        raise IndexError(
            "Message index out of range."
        )

    message = chat["messages"][
        message_index
    ]

    if message.get("role") != "assistant":

        raise ValueError(
            "Feedback can only be added to assistant messages."
        )

    message["feedback"] = feedback

    chat["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    save_chat(chat)


def save_chat(chat):

    initialize_database()

    connection = get_connection()

    messages_json = json.dumps(
        serialize_messages(
            chat["messages"]
        ),
        ensure_ascii=False,
    )

    connection.execute(
        """
        INSERT INTO chats (
            id,
            title,
            messages,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(id)
        DO UPDATE SET
            title = excluded.title,
            messages = excluded.messages,
            updated_at = excluded.updated_at
        """,
        (
            chat["id"],
            chat["title"],
            messages_json,
            chat["created_at"],
            chat["updated_at"],
        ),
    )

    connection.commit()
    connection.close()


def load_chats():

    initialize_database()

    connection = get_connection()

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

        for message in messages:

            message["sources"] = (
                deserialize_sources(
                    message.get(
                        "sources",
                        [],
                    )
                )
            )

            message.setdefault(
                "response_time",
                None,
            )

            message.setdefault(
                "feedback",
                None,
            )

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


def search_chats(
    chats,
    search_text,
):

    search_text = search_text.strip().lower()

    if not search_text:
        return chats

    matching_chats = []

    for chat in chats:

        title = chat.get(
            "title",
            "",
        ).lower()

        if search_text in title:

            matching_chats.append(chat)

            continue

        for message in chat.get(
            "messages",
            [],
        ):

            content = message.get(
                "content",
                "",
            ).lower()

            if search_text in content:

                matching_chats.append(chat)

                break

    return matching_chats


def delete_chat(
    chats,
    chat_id,
):

    remaining_chats = [
        chat
        for chat in chats
        if chat["id"] != chat_id
    ]

    initialize_database()

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats WHERE id = ?",
        (chat_id,),
    )

    connection.commit()
    connection.close()

    return remaining_chats


def delete_all_chats():

    initialize_database()

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats"
    )

    connection.commit()
    connection.close()