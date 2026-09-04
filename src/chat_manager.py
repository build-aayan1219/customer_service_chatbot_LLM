import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path


# ============================================================================
# DATABASE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "chat_history.db"


# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_connection():
    """Create a database connection."""

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

def initialize_database():
    """Create the chat database if it does not exist."""

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


# ============================================================================
# SERIALIZATION
# ============================================================================

def serialize_sources(sources):
    """Convert source documents into JSON-safe data."""

    serialized = []

    for source in sources or []:

        if hasattr(source, "page_content"):

            serialized.append(
                {
                    "page_content": source.page_content,
                }
            )

        elif isinstance(source, dict):

            serialized.append(source)

    return serialized


def deserialize_sources(sources):
    """Return stored sources in a simple dictionary format."""

    return sources or []


def serialize_messages(messages):
    """Convert messages into JSON-safe data."""

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
            }
        )

    return serialized


# ============================================================================
# CHAT CREATION
# ============================================================================

def create_chat():
    """Create a new chat object."""

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


# ============================================================================
# MESSAGE CREATION
# ============================================================================

def create_message(
    role,
    content,
    sources=None,
):
    """Create a message object."""

    return {
        "role": role,
        "content": content,
        "sources": sources or [],
    }


# ============================================================================
# CHAT TITLE
# ============================================================================

def generate_chat_title(question):
    """Generate a short title from the first question."""

    question = question.strip()

    if not question:
        return "New Chat"

    words = question.split()

    if len(words) <= 6:
        return question

    return (
        " ".join(words[:6])
        + "..."
    )


# ============================================================================
# ADD MESSAGE
# ============================================================================

def add_message(
    chat,
    role,
    content,
    sources=None,
):
    """Add a message to a chat."""

    message = create_message(
        role=role,
        content=content,
        sources=sources,
    )

    chat["messages"].append(
        message
    )

    chat["updated_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    if (
        chat["title"] == "New Chat"
        and role == "user"
    ):

        chat["title"] = (
            generate_chat_title(
                content
            )
        )

    save_chat(chat)

    return message


# ============================================================================
# FIND CHAT
# ============================================================================

def find_chat(
    chats,
    chat_id,
):
    """Find a chat by ID."""

    for chat in chats:

        if chat["id"] == chat_id:

            return chat

    return None


# ============================================================================
# DELETE CHAT
# ============================================================================

def delete_chat(
    chats,
    chat_id,
):
    """Delete a chat from memory and database."""

    remaining_chats = [
        chat
        for chat in chats
        if chat["id"] != chat_id
    ]

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats WHERE id = ?",
        (chat_id,),
    )

    connection.commit()
    connection.close()

    return remaining_chats


# ============================================================================
# RENAME CHAT
# ============================================================================

def rename_chat(
    chat,
    new_title,
):
    """Rename and save a chat."""

    new_title = new_title.strip()

    if new_title:

        chat["title"] = new_title

    chat["updated_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    save_chat(chat)

    return chat


# ============================================================================
# SAVE CHAT
# ============================================================================

def save_chat(chat):
    """Save or update a chat in SQLite."""

    initialize_database()

    connection = get_connection()

    messages_json = json.dumps(
        serialize_messages(
            chat["messages"]
        )
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


# ============================================================================
# LOAD CHATS
# ============================================================================

def load_chats():
    """Load all saved chats from SQLite."""

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


# ============================================================================
# SEARCH CHATS
# ============================================================================

def search_chats(
    chats,
    search_text,
):
    """Search chats by title and message content."""

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


# ============================================================================
# UPDATE CHAT
# ============================================================================

def update_chat(chat):
    """Save the current state of a chat."""

    chat["updated_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    save_chat(chat)

    return chat


# ============================================================================
# DATABASE CLEANUP
# ============================================================================

def delete_all_chats():
    """Delete all saved conversations."""

    initialize_database()

    connection = get_connection()

    connection.execute(
        "DELETE FROM chats"
    )

    connection.commit()
    connection.close()