from aiogram import Bot, Dispatcher
from asyncio import run
import logging

from database import create_tables
from handlers import start_router, main_router


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token='YOUR_TOKEN')
    dp = Dispatcher()

    create_tables()

    dp.include_router(start_router)
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
