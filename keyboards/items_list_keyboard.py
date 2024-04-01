from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def create_items_list_keyboard(items_list, user_id, message_id):
    keyboard = InlineKeyboardBuilder()

    for idx, item in enumerate(items_list):
        keyboard.row(InlineKeyboardButton(
            text=str(item),
            callback_data=f'{user_id}_{message_id}_{idx}')
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

