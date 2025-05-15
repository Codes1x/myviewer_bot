from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="🔹 Чаты", callback_data="show_chats")],
        [InlineKeyboardButton(text="🔹 Каналы", callback_data="show_channels")],
        [InlineKeyboardButton(text="🔹 Личные диалоги", callback_data="show_users")],
        [InlineKeyboardButton(text="🧾 Профиль", callback_data="show_profile")],  # ✅ кнопка профиля
        [InlineKeyboardButton(text="🚪 Выйти из аккаунта", callback_data="logout")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_pagination_keyboard(current_page: int, total_pages: int, base_callback: str):
    buttons = []

    if current_page > 1:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{base_callback}:{current_page - 1}"))
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"{base_callback}:{current_page + 1}"))

    if not buttons:
        return None

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def create_list_keyboard(items: list[tuple[str, str]], callback_prefix: str = "") -> InlineKeyboardMarkup:
    """
    Генерирует кнопки из списка элементов.
    :param items: Список (текст, callback_data)
    :param callback_prefix: Префикс для callback_data
    """
    keyboard = []
    for text, data in items:
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"{callback_prefix}:{data}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
