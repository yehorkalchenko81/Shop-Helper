from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def set_items_list_keyboard(user_id, message_id, items_list):
    keyboard = InlineKeyboardBuilder()

    for idx, item in enumerate(items_list):
        keyboard.row(
            InlineKeyboardButton(
                text=str(item),
                callback_data=f'edit_{user_id}_{message_id}_{idx}'
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            text='Завершити',
            callback_data=f'finish_{user_id}_{message_id}'
        )
    )

    return keyboard


def edit_items_list_keyboard(keyboard, item_idx, item):
    keyboard = keyboard.export()
    keyboard[item_idx][0].text = str(item)
    keyboard = InlineKeyboardBuilder(keyboard)

    return keyboard


main_menu_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Назад',
            callback_data='start_menu'
        )]
    ]
)