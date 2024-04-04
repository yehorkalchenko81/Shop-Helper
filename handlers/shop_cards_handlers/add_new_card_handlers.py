from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import (
    Message,
    CallbackQuery
)

from logger import logger
from states import ShopCardStates
from database import add_shop_card, read_shop_cards
from keyboards import cancel_add_button

router = Router()


@router.callback_query(F.data == 'add_card')
async def add_card(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        text='Введіть імя магазину картку якого ви хочете додати',
        reply_markup=cancel_add_button
    )

    await state.update_data(bot_message=callback.message)
    await state.set_state(ShopCardStates.waiting_shop_name)

    logger(f'{"-" * 25}\n'
           f'Func: add_card\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Time: {datetime.now()}\n'
           )


@router.message(StateFilter(ShopCardStates.waiting_shop_name), F.text)
async def catching_shop_name(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    bot_message: Message = data['bot_message']

    raw_data = read_shop_cards(message.from_user.id)
    list_shop_name = [row[0] for row in raw_data]

    if message.text in list_shop_name:
        await bot_message.edit_text(
            text='Картка цього магазину вже додана',
            reply_markup=cancel_add_button
        )

        return await state.clear()

    await state.update_data(shop_name=message.text)

    await bot_message.delete()

    bot_message = await message.answer(
        text='Відправте карту магазину фотографією',
        reply_markup=cancel_add_button
    )

    await state.update_data(bot_message=bot_message)

    await state.set_state(ShopCardStates.waiting_shop_card)

    logger(f'{"-" * 25}\n'
           f'Func: catching_shop_name\n'
           f'User_id: {message.from_user.id}\n'
           f'User_name: {message.from_user.full_name}\n'
           f'User_input: {message.text}\n'
           f'Time: {datetime.now()}\n'
           )


@router.message(StateFilter(ShopCardStates.waiting_shop_card), F.photo)
async def waiting_shop_card(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    shop_name = data['shop_name']
    bot_message = data['bot_message']

    await bot_message.delete()

    await message.answer(
        text='Картку додано',
        reply_markup=cancel_add_button
    )

    add_shop_card(message.from_user.id, shop_name, message.photo[-1].file_id)

    await state.clear()

    logger(f'{"-" * 25}\n'
           f'Func: show_card_list\n'
           f'User_id: {message.from_user.id}\n'
           f'User_name: {message.from_user.full_name}\n'
           f'User_photo: {message.photo[-1].file_id}\n'
           f'Time: {datetime.now()}\n'
           )


@router.message(StateFilter(ShopCardStates))
async def delete_wrong_type(message: Message, state: FSMContext):
    await message.delete()
