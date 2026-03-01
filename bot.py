from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from asyncio import run
import messages
import logging
from utils.database import init_db

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

async def main():
    bot = Bot(token=BOT_TOKEN)
    await init_db()
    dp.include_router(messages.router)

    await dp.start_polling(bot)

run(main())