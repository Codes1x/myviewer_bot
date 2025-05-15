from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.utils.client_manager import disconnect_client, delete_session

router = Router()

@router.callback_query(F.data == "logout")
async def logout_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    try:
        # 1. Отключаем Telethon-клиент
        await disconnect_client(user_id)

        # 2. Удаляем session-файл
        delete_session(user_id)

        # 3. Возврат к /start
        await callback.message.edit_text("✅ Вы вышли из аккаунта.\nЧтобы авторизоваться снова — отправьте /start.")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при выходе из аккаунта: {e}")
