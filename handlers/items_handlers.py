from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

from keyboards import set_items_list_keyboard, edit_items_list_keyboard
from utils import ItemsList
from database import (
    create_item_list,
    read_item_list,
    edit_item_list,
    remove_item_list
)

router = Router()


@router.message(F.text)
async def shop_list(message: Message):
    await message.delete()

    user_id = message.from_user.id
    message_id = message.message_id
    items_list = ItemsList(message.text)

    keyboard = set_items_list_keyboard(user_id, message_id, items_list)

    await message.answer(
        text='Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    create_item_list(user_id, message_id, items_list, keyboard)


@router.callback_query(F.data.contains('edit_'))
async def edit_item(callback: CallbackQuery):
    _, user_id, message_id, item_idx = callback.data.split('_')
    item_idx = int(item_idx)

    items_list, keyboard = read_item_list(user_id, message_id)
    item = items_list[item_idx]

    item.remove() if item.is_added else item.add()

    keyboard = edit_items_list_keyboard(keyboard, item_idx, item)

    await callback.message.edit_text(
        text='Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()

    edit_item_list(user_id, message_id, items_list, keyboard)


@router.callback_query(F.data.contains('finish_'))
async def finish(callback: CallbackQuery):
    _, user_id, message_id = callback.data.split('_')
    items_list, _ = read_item_list(user_id, message_id)

    remove_item_list(user_id, message_id)

    await callback.message.edit_text(
        text=f'Ваш список покупок:\n{str(items_list)}'
    )

    await callback.answer()


@router.message()
async def shop_list(message: Message):
    await message.delete()
