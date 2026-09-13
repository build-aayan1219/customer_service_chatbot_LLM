import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "chat_history.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
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
        for row in connection.execute("PRAGMA table_info(chats)").fetchall()
    }
    if "pinned" not in columns:
        connection.execute("ALTER TABLE chats ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0")
    if "archived" not in columns:
        connection.execute("ALTER TABLE chats ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
    connection.commit()
    connection.close()


def serialize_sources(sources):
    serialized = []
    for source in sources or []:
        if hasattr(source, "page_content"):
            serialized.append({
                "page_content": source.page_content,
                "metadata": getattr(source, "metadata", {}),
            })
        elif isinstance(source, dict):
            serialized.append({
                "page_content": source.get("page_content", ""),
                "metadata": source.get("metadata", {}),
            })
    return serialized


def deserialize_sources(sources):
    return sources or []


def serialize_messages(messages):
    serialized = []
    for message in messages:
        serialized.append({
            "role": message.get("role", ""),
            "content": message.get("content", ""),
            "sources": serialize_sources(message.get("sources", [])),
            "response_time": message.get("response_time"),
            "feedback": message.get("feedback"),
        })
    return serialized


def create_chat():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat = {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": [],
        "created_at": now,
        "updated_at": now,
        "pinned": False,
        "archived": False,
    }
    save_chat(chat)
    return chat


def create_message(role, content, sources=None, response_time=None, feedback=None):
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
    if len(words) <= 7:
        return question
    return " ".join(words[:7]) + "..."


def add_message(chat, role, content, sources=None, response_time=None, feedback=None):
    message = create_message(role, content, sources, response_time, feedback)
    chat["messages"].append(message)
    chat["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if chat.get("title", "New Chat") == "New Chat" and role == "user":
        chat["title"] = generate_chat_title(content)
    save_chat(chat)
    return message


def update_chat(chat):
    chat["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_chat(chat)
    return chat


def find_chat(chats, chat_id):
    for chat in chats:
        if chat["id"] == chat_id:
            return chat
    return None


def rename_chat(chat, new_title):
    new_title = new_title.strip()
    if new_title:
        chat["title"] = new_title
    return update_chat(chat)


def set_chat_pinned(chat, pinned=True):
    chat["pinned"] = bool(pinned)
    return update_chat(chat)


def set_chat_archived(chat, archived=True):
    chat["archived"] = bool(archived)
    return update_chat(chat)


def truncate_chat(chat, message_index):
    if message_index < 0 or message_index >= len(chat.get("messages", [])):
        raise IndexError("Message index out of range.")
    chat["messages"] = chat["messages"][:message_index]
    if not chat["messages"]:
        chat["title"] = "New Chat"
    return update_chat(chat)


def remove_message(chat, message_index):
    if message_index < 0 or message_index >= len(chat.get("messages", [])):
        raise IndexError("Message index out of range.")
    chat["messages"].pop(message_index)
    return update_chat(chat)


def update_message_feedback(chat, message_index, feedback):
    allowed_feedback = {"positive", "negative", None}
    if feedback not in allowed_feedback:
        raise ValueError("Invalid feedback value.")
    if message_index < 0 or message_index >= len(chat["messages"]):
        raise IndexError("Message index out of range.")
    message = chat["messages"][message_index]
    if message.get("role") != "assistant":
        raise ValueError("Feedback can only be added to assistant messages.")
    message["feedback"] = feedback
    update_chat(chat)


def save_chat(chat):
    initialize_database()
    connection = get_connection()
    messages_json = json.dumps(serialize_messages(chat.get("messages", [])), ensure_ascii=False)
    connection.execute(
        """
        INSERT INTO chats (id, title, messages, created_at, updated_at, pinned, archived)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            messages = excluded.messages,
            updated_at = excluded.updated_at,
            pinned = excluded.pinned,
            archived = excluded.archived
        """,
        (
            chat["id"],
            chat.get("title", "New Chat"),
            messages_json,
            chat.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            chat.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            int(bool(chat.get("pinned", False))),
            int(bool(chat.get("archived", False))),
        ),
    )
    connection.commit()
    connection.close()


def load_chats(include_archived=True):
    initialize_database()
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, title, messages, created_at, updated_at, pinned, archived
        FROM chats
        ORDER BY pinned DESC, updated_at DESC
        """
    ).fetchall()
    connection.close()

    chats = []
    for row in rows:
        if not include_archived and row["archived"]:
            continue
        try:
            messages = json.loads(row["messages"])
        except (json.JSONDecodeError, TypeError):
            messages = []
        for message in messages:
            message["sources"] = deserialize_sources(message.get("sources", []))
            message.setdefault("response_time", None)
            message.setdefault("feedback", None)
        chats.append({
            "id": row["id"],
            "title": row["title"],
            "messages": messages,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "pinned": bool(row["pinned"]),
            "archived": bool(row["archived"]),
        })
    return chats


def search_chats(chats, search_text):
    search_text = search_text.strip().lower()
    if not search_text:
        return chats
    matching = []
    for chat in chats:
        if search_text in chat.get("title", "").lower():
            matching.append(chat)
            continue
        for message in chat.get("messages", []):
            if search_text in message.get("content", "").lower():
                matching.append(chat)
                break
    return matching


def delete_chat(chats, chat_id):
    remaining = [chat for chat in chats if chat["id"] != chat_id]
    initialize_database()
    connection = get_connection()
    connection.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
    connection.commit()
    connection.close()
    return remaining


def delete_all_chats():
    initialize_database()
    connection = get_connection()
    connection.execute("DELETE FROM chats")
    connection.commit()
    connection.close()
