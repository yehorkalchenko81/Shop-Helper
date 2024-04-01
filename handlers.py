from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardRemove, CallbackQuery
from classes import ItemsList
from aiogram import F
from database import add_new_user, create_item_list, edit_item_list, remove_item_list, read_item_list

from bot import dp


async def start(message: Message):
    add_new_user(message.from_user.id, message.from_user.full_name)
    await message.answer(
        'Відправ мені список одним повідомленням!',
        reply_markup=ReplyKeyboardRemove()
    )


async def shop_list(message: Message):
    keyboard = InlineKeyboardBuilder()
    items_list = ItemsList(message.text)
    user_id = message.from_user.id
    message_id = message.message_id
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

    await message.answer(
        'Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    create_item_list(user_id, message_id, items_list, keyboard)


async def call_back(callback: CallbackQuery):
    if 'finish_' in callback.data:
        await finish(callback)
    else:
        await edit_item(callback)


async def edit_item(callback: CallbackQuery):
    user_id, message_id, item_idx = callback.data.split('_')
    items_list, keyboard = read_item_list(user_id, message_id)
    item = items_list[int(item_idx)]

    item.remove() if item.is_added else item.add()

    keyboard = keyboard.export()
    keyboard[int(item_idx)][0].text = str(item)
    keyboard = InlineKeyboardBuilder(keyboard)

    await callback.message.edit_text(
        text='Ваш список покупок:',
        inline_message_id=message_id,
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()

    edit_item_list(user_id, message_id, items_list, keyboard)


async def finish(callback: CallbackQuery):
    _, user_id, message_id = callback.data.split('_')
    items_list, *_ = read_item_list(user_id, message_id)
    remove_item_list(user_id, message_id)

    await callback.message.edit_text(
        text=f'Ваш список покупок:\n{str(items_list)}',
        inline_message_id=message_id
    )

    await callback.answer()


def start_handlers():
    dp.message.register(start, Command('start'))
    dp.message.register(shop_list, F.text)
    dp.callback_query.register(call_back, F.data)
