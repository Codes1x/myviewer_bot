from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    PhoneNumberBannedError,
    FloodWaitError,
    AuthRestartError,
    RPCError,
)
import asyncio

def map_telethon_error(exc: Exception) -> str:
    """
    Преобразует ошибки Telethon в читаемые сообщения для пользователя.
    """
    if isinstance(exc, PhoneCodeInvalidError):
        return "❌ Неверный код подтверждения. Попробуйте ещё раз."
    elif isinstance(exc, PhoneCodeExpiredError):
        return "⌛ Код подтверждения истёк. Запросите новый код."
    elif isinstance(exc, PhoneNumberBannedError):
        return "🚫 Этот номер был заблокирован Telegram. Используйте другой номер."
    elif isinstance(exc, SessionPasswordNeededError):
        return "🔐 Требуется двухфакторная аутентификация. Введите пароль."
    elif isinstance(exc, FloodWaitError):
        return f"⚠️ Слишком много запросов. Подождите {exc.seconds} сек."
    elif isinstance(exc, AuthRestartError):
        return "🔄 Сессия сброшена. Попробуйте заново."
    elif isinstance(exc, asyncio.TimeoutError):
        return "⏱ Истекло время ожидания ответа от Telegram. Повторите попытку."
    elif isinstance(exc, RPCError):
        return f"⚠️ Ошибка Telegram API: {exc.MESSAGE}"
    else:
        return f"⚠️ Неизвестная ошибка: {str(exc)}"
