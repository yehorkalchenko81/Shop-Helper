from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Мої картки',
                callback_data='view_my_cards'
            )
        ],
        [
            InlineKeyboardButton(
                text='Додати список',
                callback_data='new_items_list'
            )
        ]
    ]
)
