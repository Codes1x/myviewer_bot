from aiogram import Router, F
from aiogram.types import CallbackQuery
from math import ceil

from bot.utils.client_manager import get_client_for_user
from bot.keyboards.inline import get_pagination_keyboard
from bot.utils.errors import map_telethon_error 

router = Router()
PER_PAGE = 10

@router.callback_query(F.data.startswith("show_users"))
async def show_users(callback: CallbackQuery):
    try:
        # Получаем страницу из callback_data
        page = 1
        if ":" in callback.data:
            _, page = callback.data.split(":")
            page = int(page)

        user_id = callback.from_user.id
        client = await get_client_for_user(user_id, create_if_missing=False)

        if not client:
            await callback.message.answer("❗️Сначала авторизуйтесь.")
            return

        await client.connect()
        dialogs = await client.get_dialogs()
        users = [d for d in dialogs if d.is_user]

        if not users:
            await callback.message.edit_text("ℹ️ У вас пока нет личных диалогов.")
            return

        total_pages = ceil(len(users) / PER_PAGE)
        offset = (page - 1) * PER_PAGE
        items = users[offset:offset + PER_PAGE]

        text = "<b>👤 Личные диалоги:</b>\n\n"
        for user in items:
            name = user.name or "Без имени"
            text += f"👤 <b>{name}</b> — <code>{user.id}</code>\n"

        keyboard = get_pagination_keyboard(page, total_pages, base_callback="show_users")

        await callback.message.edit_text(text, reply_markup=keyboard)

    except Exception as e:
        error_text = map_telethon_error(e)
        await callback.message.answer(error_text)
