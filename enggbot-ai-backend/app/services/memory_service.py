"""
Memory Service

Stores conversation history for each user.
Currently uses in-memory storage.
Can later be replaced with PostgreSQL/Redis
without changing the public API.
"""

from collections import defaultdict

# Maximum number of messages to keep per user
MAX_HISTORY = 50

conversation_memory = defaultdict(list)


def save_message(user_id, role, content):
    """
    Save a chat message.
    """

    if not user_id:
        return

    if role not in ("user", "assistant", "system"):
        role = "assistant"

    if content is None:
        return

    content = str(content).strip()

    if not content:
        return

    conversation_memory[user_id].append({
        "role": role,
        "content": content
    })

    # Keep only the latest MAX_HISTORY messages
    if len(conversation_memory[user_id]) > MAX_HISTORY:
        conversation_memory[user_id] = conversation_memory[user_id][-MAX_HISTORY:]


def get_history(user_id):
    """
    Return a copy of the user's conversation history.
    """

    return conversation_memory.get(user_id, []).copy()


def clear_history(user_id):
    """
    Remove all stored messages for a user.
    """

    conversation_memory.pop(user_id, None)