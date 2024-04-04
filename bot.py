from asyncio import run

from database import create_tables
from create_bot import bot, dp
from handlers import (
    start_router,
    items_router,
    show_cards_router,
    add_new_card_router,
    shop_cards_operations_router,
    trash_router
)


async def main():
    create_tables()

    dp.include_router(start_router)
    dp.include_router(show_cards_router)
    dp.include_router(add_new_card_router)
    dp.include_router(shop_cards_operations_router)
    dp.include_router(items_router)
    dp.include_router(trash_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
