import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bot.handlers import start, auth, chats, channels, users, logout, profile


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")


from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())


from bot.handlers import start, auth, chats, channels, users



def register_all_handlers():
    dp.include_router(start.router)
    dp.include_router(auth.router)
    dp.include_router(chats.router)
    dp.include_router(channels.router)
    dp.include_router(users.router)
    dp.include_router(logout.router)
    dp.include_router(profile.router)


async def main():
    logger.info("Запуск бота...")
    register_all_handlers()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
