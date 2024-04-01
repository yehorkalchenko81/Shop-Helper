from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

from database import create_item_list, read_item_list, edit_item_list, remove_item_list
from logic import ItemsList
from keyboards import create_items_list_keyboard, edit_items_list_keyboard

main_router = Router()


@main_router.message(F.text)
async def shop_list(message: Message):
    user_id = message.from_user.id
    message_id = message.message_id
    items_list = ItemsList(message.text)

    keyboard = create_items_list_keyboard(items_list, user_id, message_id)

    await message.answer(
        text='Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    create_item_list(user_id, message_id, items_list, keyboard)


@main_router.callback_query(F.data)
async def call_back(callback: CallbackQuery):
    if callback.data.startswith('finish_'):
        await finish(callback)
    else:
        await edit_item(callback)


async def edit_item(callback: CallbackQuery):
    user_id, message_id, item_idx = callback.data.split('_')
    item_idx = int(item_idx)

    items_list, keyboard = read_item_list(user_id, message_id)
    item = items_list[item_idx]

    item.remove() if item.is_added else item.add()

    keyboard = edit_items_list_keyboard(keyboard, item_idx, item)

    await callback.message.edit_text(
        text='Ваш список покупок:',
        inline_message_id=message_id,
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()

    edit_item_list(user_id, message_id, items_list, keyboard)


async def finish(callback: CallbackQuery):
    _, user_id, message_id = callback.data.split('_')
    items_list, _ = read_item_list(user_id, message_id)

    remove_item_list(user_id, message_id)

    await callback.message.edit_text(
        text=f'Ваш список покупок:\n{str(items_list)}',
        inline_message_id=message_id
    )

    await callback.answer()
