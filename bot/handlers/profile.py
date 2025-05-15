from aiogram import Router, F
from aiogram.types import CallbackQuery, InputFile
from bot.utils.client_manager import get_client_for_user
from bot.utils.errors import map_telethon_error
import os

router = Router()

@router.callback_query(F.data == "show_profile")
async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id

    try:
        client = await get_client_for_user(user_id, create_if_missing=False)
        if not client:
            await callback.message.answer("❗️Сначала авторизуйтесь.")
            return

        await client.connect()
        me = await client.get_me()

        # Сбор текстовой информации
        profile_text = (
            "<b>🧾 Профиль Telegram:</b>\n\n"
            f"👤 Имя: <b>{me.first_name or ''} {me.last_name or ''}</b>\n"
            f"📛 Username: @{me.username if me.username else '—'}\n"
            f"🆔 ID: <code>{me.id}</code>\n"
            f"📱 Телефон: +{me.phone}\n"
            f"✅ Premium: {'Да' if me.premium else 'Нет'}"
        )

       
        if me.photo:
            photo_file = f"sessions/{user_id}_avatar.jpg"
            await client.download_profile_photo(me, file=photo_file)
            await callback.message.answer_photo(photo=InputFile(photo_file), caption=profile_text)
            os.remove(photo_file)  # Чистим после отправки
        else:
            await callback.message.answer(profile_text)

    except Exception as e:
        error_text = map_telethon_error(e)
        await callback.message.answer(error_text)
