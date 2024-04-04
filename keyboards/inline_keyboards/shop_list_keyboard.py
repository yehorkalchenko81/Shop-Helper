from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import read_shop_cards


def set_shop_cards_keyboard(user_id):
    raw_data = read_shop_cards(user_id)
    list_shop_name = [row[0] for row in raw_data]

    keyboard = InlineKeyboardBuilder()

    for shop_name in list_shop_name:
        keyboard.row(
            InlineKeyboardButton(
                text=shop_name,
                callback_data=f'viewcard_{shop_name}'
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                text='❌',
                callback_data=f'delcard_{shop_name}'
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            text='Додати картку',
            callback_data=f'add_card'
        )
    )

    return keyboard


confirmating_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='✅',
            callback_data='deleting_confirmed'
        ),
        InlineKeyboardButton(
            text='❌',
            callback_data='deleting_canceled'
        )
    ]
]
)
