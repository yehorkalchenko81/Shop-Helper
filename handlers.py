from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardRemove, CallbackQuery, KeyboardButton
from classes import ItemsList
from aiogram import F

from bot import dp


async def start(message: Message):
    await message.answer(
        'Відправ мені список одним повідомленням!',
        reply_markup=ReplyKeyboardRemove()
    )


async def shop_list(message: Message):
    keyboard = InlineKeyboardBuilder()
    items_list = ItemsList(message.text)
    for idx, item in enumerate(items_list):
        keyboard.row(InlineKeyboardButton(
            text=str(item),
            callback_data=str(idx))
        )

    keyboard.row(
        InlineKeyboardButton(
            text='Завершити',
            callback_data='finish'
        )
    )

    await message.answer(
        'Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    dp['items_list'] = items_list
    dp['message_id'] = message.message_id


async def edit_item(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    message_id = dp['message_id']
    items_list = dp['items_list']
    item_idx = int(callback.data)
    item = items_list[item_idx]

    if item.is_added:
        item.remove()
    else:
        item.add()

    for idx, item in enumerate(items_list):
        keyboard.row(InlineKeyboardButton(
            text=str(item),
            callback_data=str(idx))
        )

    keyboard.row(
        InlineKeyboardButton(
            text='Завершити',
            callback_data='finish'
        )
    )

    await callback.message.edit_text(
        text='Ваш список покупок:',
        inline_message_id=str(message_id),
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()

    dp['items_list'] = items_list


async def finish(callback: CallbackQuery):
    message_id = dp['message_id']
    items_list = dp['items_list']

    await callback.message.edit_text(
        text=f'Ваш список покупок:\n{str(items_list)}',
        inline_message_id=str(message_id)
    )

    await callback.answer()


def start_handlers():
    dp.message.register(start, Command('start'))
    dp.message.register(shop_list, F.text)
    dp.callback_query.register(finish, F.data == 'finish')
    dp.callback_query.register(edit_item, F.data)
