from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.utils.errors import map_telethon_error
from bot.utils.client_manager import get_client_for_user
from bot.keyboards.inline import get_main_menu

from telethon.errors import SessionPasswordNeededError

router = Router()

class AuthStates(StatesGroup):
    awaiting_phone = State()
    awaiting_code = State()
    awaiting_2fa = State()

@router.message(F.text.regexp(r"^\+\d{11,15}$"))
async def handle_phone(message: Message, state: FSMContext):
    await state.set_state(AuthStates.awaiting_code)
    phone = message.text.strip()
    await state.update_data(phone=phone)

    user_id = message.from_user.id

    try:
        client = await get_client_for_user(user_id, phone=phone, create_if_missing=True)
        await client.connect()
        await client.send_code_request(phone)
        await message.answer("📩 Введите код подтверждения, полученный в Telegram:")
    except Exception as e:
        error_text = map_telethon_error(e)
        await message.answer(error_text)
        await state.clear()

@router.message(AuthStates.awaiting_code)
async def handle_code(message: Message, state: FSMContext):
    code = message.text.strip()
    data = await state.get_data()
    phone = data.get("phone")
    user_id = message.from_user.id

    try:
        client = await get_client_for_user(user_id, phone=phone)
        await client.sign_in(phone=phone, code=code)
        await message.answer("✅ Авторизация прошла успешно! Выберите действие:", reply_markup=get_main_menu())
        await state.clear()
    except SessionPasswordNeededError:
        await message.answer("🔐 У вас включена двухфакторная аутентификация. Введите пароль:")
        await state.set_state(AuthStates.awaiting_2fa)
    except Exception as e:
        error_text = map_telethon_error(e)
        await message.answer(error_text)
        await state.clear()

@router.message(AuthStates.awaiting_2fa)
async def handle_2fa(message: Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    phone = data.get("phone")
    user_id = message.from_user.id

    try:
        client = await get_client_for_user(user_id, phone=phone)
        await client.sign_in(password=password)
        await message.answer("✅ Авторизация завершена! Выберите действие:", reply_markup=get_main_menu())
        await state.clear()
    except Exception as e:
        error_text = map_telethon_error(e)
        await message.answer(error_text)
        await state.clear()
