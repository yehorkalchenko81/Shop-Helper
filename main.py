from handlers import start_handlers
from bot import dp, bot
from asyncio import run


async def main():
    start_handlers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
