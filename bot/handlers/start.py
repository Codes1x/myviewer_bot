from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import get_main_menu
from bot.utils.client_manager import get_client_for_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Проверяем наличие сессии
    client = await get_client_for_user(user_id, create_if_missing=False)

    if client:
        await message.answer("✅ Вы уже авторизованы. Выберите действие:", reply_markup=get_main_menu())
    else:
        await message.answer("👋 Привет! Введите свой номер телефона (в формате +79001234567) для авторизации в Telegram:")
        await state.set_state("awaiting_phone")
