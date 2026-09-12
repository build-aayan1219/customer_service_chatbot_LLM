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
            updated_at TEXT NOT NULL,
            pinned INTEGER NOT NULL DEFAULT 0,
            archived INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    columns = {
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(chats)"
        ).fetchall()
    }

    if "pinned" not in columns:
        connection.execute(
            """
            ALTER TABLE chats
            ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0
            """
        )

    if "archived" not in columns:
        connection.execute(
            """
            ALTER TABLE chats
            ADD COLUMN archived INTEGER NOT NULL DEFAULT 0
            """
        )

    connection.commit()
    connection.close()


def serialize_sources(sources):
    serialized = []

    for source in sources or []:

        if hasattr(source, "page_content"):

            metadata = getattr(
                source,
                "metadata",
                {},
            )

            if not isinstance(metadata, dict):
                metadata = {}

            serialized.append(
                {
                    "page_content": str(
                        source.page_content or ""
                    ),
                    "metadata": metadata,
                }
            )

        elif isinstance(source, dict):

            metadata = source.get(
                "metadata",
                {},
            )

            if not isinstance(metadata, dict):
                metadata = {}

            serialized.append(
                {
                    "page_content": str(
                        source.get(
                            "page_content",
                            source.get(
                                "content",
                                "",
                            ),
                        )
                        or ""
                    ),
                    "metadata": metadata,
                }
            )

    return serialized


def deserialize_sources(sources):
    if not isinstance(sources, list):
        return []

    return sources


def serialize_messages(messages):
    serialized = []

    for message in messages or []:

        if not isinstance(message, dict):
            continue

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
        "pinned": False,
        "archived": False,
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
        "content": str(content or ""),
        "sources": sources or [],
        "response_time": response_time,
        "feedback": feedback,
    }


def generate_chat_title(question):
    question = str(
        question or ""
    ).strip()

    if not question:
        return "New Chat"

    words = question.split()

    if len(words) <= 7:
        return question

    return (
        " ".join(words[:7])
        + "..."
    )


def add_message(
    chat,
    role,
    content,
    sources=None,
    response_time=None,
    feedback=None,
):
    if "messages" not in chat:
        chat["messages"] = []

    message = create_message(
        role=role,
        content=content,
        sources=sources,
        response_time=response_time,
        feedback=feedback,
    )

    chat["messages"].append(
        message
    )

    chat["updated_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if (
        chat.get("title") == "New Chat"
        and role == "user"
    ):
        chat["title"] = generate_chat_title(
            content
        )

    save_chat(chat)

    return message


def find_chat(
    chats,
    chat_id,
):
    if not chat_id:
        return None

    for chat in chats or []:

        if chat.get("id") == chat_id:
            return chat

    return None


def rename_chat(
    chat,
    new_title,
):
    new_title = str(
        new_title or ""
    ).strip()

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

    messages = chat.get(
        "messages",
        [],
    )

    if (
        message_index < 0
        or message_index >= len(messages)
    ):
        raise IndexError(
            "Message index out of range."
        )

    message = messages[
        message_index
    ]

    if message.get("role") != "assistant":
        raise ValueError(
            "Feedback can only be added to assistant messages."
        )

    message["feedback"] = feedback

    update_chat(chat)


def set_chat_pinned(
    chat,
    pinned,
):
    chat["pinned"] = bool(
        pinned
    )

    update_chat(chat)

    return chat


def set_chat_archived(
    chat,
    archived,
):
    chat["archived"] = bool(
        archived
    )

    update_chat(chat)

    return chat


def truncate_chat(
    chat,
    message_index,
):
    messages = chat.get(
        "messages",
        [],
    )

    if message_index < 0:
        message_index = 0

    chat["messages"] = messages[
        :message_index
    ]

    if not chat["messages"]:
        chat["title"] = "New Chat"

    update_chat(chat)

    return chat


def remove_message(
    chat,
    message_index,
):
    messages = chat.get(
        "messages",
        [],
    )

    if (
        message_index < 0
        or message_index >= len(messages)
    ):
        return False

    messages.pop(
        message_index
    )

    if not messages:
        chat["title"] = "New Chat"

    update_chat(chat)

    return True


def save_chat(chat):
    initialize_database()

    connection = get_connection()

    messages_json = json.dumps(
        serialize_messages(
            chat.get(
                "messages",
                [],
            )
        ),
        ensure_ascii=False,
    )

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    chat_id = str(
        chat.get(
            "id",
            uuid.uuid4(),
        )
    )

    title = str(
        chat.get(
            "title",
            "New Chat",
        )
    )

    created_at = str(
        chat.get(
            "created_at",
            now,
        )
    )

    updated_at = str(
        chat.get(
            "updated_at",
            now,
        )
    )

    pinned = int(
        bool(
            chat.get(
                "pinned",
                False,
            )
        )
    )

    archived = int(
        bool(
            chat.get(
                "archived",
                False,
            )
        )
    )

    connection.execute(
        """
        INSERT INTO chats (
            id,
            title,
            messages,
            created_at,
            updated_at,
            pinned,
            archived
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(id)
        DO UPDATE SET
            title = excluded.title,
            messages = excluded.messages,
            updated_at = excluded.updated_at,
            pinned = excluded.pinned,
            archived = excluded.archived
        """,
        (
            chat_id,
            title,
            messages_json,
            created_at,
            updated_at,
            pinned,
            archived,
        ),
    )

    connection.commit()
    connection.close()


def load_chats(
    include_archived=True,
):
    initialize_database()

    connection = get_connection()

    if include_archived:

        rows = connection.execute(
            """
            SELECT
                id,
                title,
                messages,
                created_at,
                updated_at,
                pinned,
                archived
            FROM chats
            ORDER BY
                pinned DESC,
                updated_at DESC
            """
        ).fetchall()

    else:

        rows = connection.execute(
            """
            SELECT
                id,
                title,
                messages,
                created_at,
                updated_at,
                pinned,
                archived
            FROM chats
            WHERE archived = 0
            ORDER BY
                pinned DESC,
                updated_at DESC
            """
        ).fetchall()

    connection.close()

    chats = []

    for row in rows:

        try:
            messages = json.loads(
                row["messages"]
            )

            if not isinstance(
                messages,
                list,
            ):
                messages = []

        except (
            json.JSONDecodeError,
            TypeError,
        ):
            messages = []

        cleaned_messages = []

        for message in messages:

            if not isinstance(
                message,
                dict,
            ):
                continue

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

            message.setdefault(
                "role",
                "",
            )

            message.setdefault(
                "content",
                "",
            )

            cleaned_messages.append(
                message
            )

        chats.append(
            {
                "id": row["id"],
                "title": row["title"],
                "messages": cleaned_messages,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "pinned": bool(
                    row["pinned"]
                ),
                "archived": bool(
                    row["archived"]
                ),
            }
        )

    return chats


def search_chats(
    chats,
    search_text,
):
    search_text = str(
        search_text or ""
    ).strip().lower()

    if not search_text:
        return chats

    matching_chats = []

    for chat in chats or []:

        title = str(
            chat.get(
                "title",
                "",
            )
        ).lower()

        if search_text in title:
            matching_chats.append(
                chat
            )
            continue

        for message in chat.get(
            "messages",
            [],
        ):

            content = str(
                message.get(
                    "content",
                    "",
                )
            ).lower()

            if search_text in content:
                matching_chats.append(
                    chat
                )
                break

    return matching_chats


def delete_chat(
    chats,
    chat_id,
):
    remaining_chats = [
        chat
        for chat in chats or []
        if chat.get("id") != chat_id
    ]

    initialize_database()

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats WHERE id = ?",
        (
            chat_id,
        ),
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