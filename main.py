from handlers import start_handlers
from bot import dp, bot
from asyncio import run
from database import create_table


async def main():
    create_table()
    start_handlers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
