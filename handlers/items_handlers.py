from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from datetime import datetime

from keyboards import set_items_list_keyboard, edit_items_list_keyboard, main_menu_button
from states import ItemsListState
from utils import ItemsList
from logger import logger
from database import (
    create_item_list,
    read_item_list,
    edit_item_list,
    remove_item_list
)

router = Router()


@router.callback_query(StateFilter(None), F.data == 'new_items_list')
async def new_items_list(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Напишіть список одним повідомленням',
        reply_markup=main_menu_button
    )
    await state.update_data(bot_message=callback.message)
    await state.set_state(ItemsListState.waiting_items_list)

    logger(f'{"-" * 25}\n'
           f'Func: new_items_list\n\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Time: {datetime.now()}\n'
           )


@router.message(StateFilter(ItemsListState.waiting_items_list), F.text)
async def shop_list(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message: Message = data['bot_message']
    await bot_message.delete()
    await message.delete()
    await state.clear()

    user_id = message.from_user.id
    message_id = message.message_id
    items_list = ItemsList(message.text)

    keyboard = set_items_list_keyboard(user_id, message_id, items_list)

    await message.answer(
        text='Ваш список покупок:',
        reply_markup=keyboard.as_markup()
    )

    create_item_list(user_id, message_id, items_list, keyboard)

    logger(f'{"-" * 25}\n'
           f'Func: shop_list\n'
           f'User_id: {message.from_user.id}\n'
           f'User_name: {message.from_user.full_name}\n'
           f'User_input: {message.text}\n'
           f'Time: {datetime.now()}\n'
           )


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

    logger(f'{"-" * 25}\n'
           f'Func: edit_item\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Items_list: {str(items_list)}\n'
           f'Time: {datetime.now()}\n'
           )


@router.callback_query(F.data.contains('finish_'))
async def finish(callback: CallbackQuery):
    _, user_id, message_id = callback.data.split('_')
    items_list, _ = read_item_list(user_id, message_id)

    remove_item_list(user_id, message_id)

    await callback.message.edit_text(
        text=f'Ваш список покупок:\n{str(items_list)}',
        reply_markup=main_menu_button
    )

    await callback.answer()

    logger(f'{"-" * 25}\n'
           f'Func: finish\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Items_list: {str(items_list)}\n'
           f'Time: {datetime.now()}\n'
           )

#
# @router.message(F.text == 'ADMIN')
# async def admin(message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAIDimYOtVdcMLV-EVy7AWG-zkyj65E6AALW3TEbGL95SLtudidRU7U8AQADAgADeQADNAQ')
