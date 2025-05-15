import os
from telethon import TelegramClient

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

sessions_dir = "sessions"
os.makedirs(sessions_dir, exist_ok=True)

_clients = {}

async def get_client_for_user(user_id: int, phone: str = None, create_if_missing=True) -> TelegramClient | None:
    """
    Получает или создает Telethon-клиент для пользователя.
    """
    session_path = os.path.join(sessions_dir, f"{user_id}")

    if user_id in _clients:
        return _clients[user_id]

 
    if not create_if_missing and not os.path.exists(session_path + ".session"):
        return None

  
    client = TelegramClient(session_path, API_ID, API_HASH)
    _clients[user_id] = client
    return client

async def disconnect_client(user_id: int):
    client = _clients.get(user_id)
    if client:
        await client.disconnect()
        del _clients[user_id]

def delete_session(user_id: int):
    session_path = os.path.join(sessions_dir, f"{user_id}.session")
    if os.path.exists(session_path):
        os.remove(session_path)
