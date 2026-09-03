import uuid
from datetime import datetime


def create_chat():
    return {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def create_message(role, content, sources=None):
    return {
        "role": role,
        "content": content,
        "sources": sources or [],
    }


def generate_chat_title(question):
    question = question.strip()

    if not question:
        return "New Chat"

    words = question.split()

    if len(words) <= 6:
        return question

    return " ".join(words[:6]) + "..."


def add_message(chat, role, content, sources=None):
    message = create_message(
        role=role,
        content=content,
        sources=sources,
    )

    chat["messages"].append(message)
    chat["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if chat["title"] == "New Chat" and role == "user":
        chat["title"] = generate_chat_title(content)

    return message


def find_chat(chats, chat_id):
    for chat in chats:
        if chat["id"] == chat_id:
            return chat

    return None


def delete_chat(chats, chat_id):
    return [
        chat
        for chat in chats
        if chat["id"] != chat_id
    ]


def rename_chat(chat, new_title):
    new_title = new_title.strip()

    if new_title:
        chat["title"] = new_title

    chat["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return chat