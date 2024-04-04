from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove
)

from states import ShopCardStates
from database import add_shop_card, read_shop_cards
from keyboards import cancel_fsm_button, view_my_cards_button
from .show_shop_cards_handler import show_card_list

router = Router()


@router.callback_query(StateFilter(None), F.data == 'add_card')
async def add_card(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    bot_message = await callback.message.answer(
        text='Введіть імя магазину картку якого ви хочете додати',
        reply_markup=cancel_fsm_button
    )

    await state.update_data(bot_message=bot_message)
    await state.set_state(ShopCardStates.waiting_shop_name)


@router.message(StateFilter(ShopCardStates), F.text == 'Відмінити')
async def stop_adding_card(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message = data['bot_message']

    await bot_message.delete()

    await state.clear()

    await show_card_list(message)


@router.message(StateFilter(ShopCardStates.waiting_shop_name), F.text)
async def catching_shop_name(message: Message, state: FSMContext):
    raw_data = read_shop_cards(message.from_user.id)

    list_shop_name = [row[0] for row in raw_data]

    if message.text in list_shop_name:
        await message.answer(
            text='Картка цього магазину вже додана',
            reply_markup=ReplyKeyboardRemove()
        )

        await state.clear()
        return await show_card_list(message)

    await message.delete()

    await state.update_data(shop_name=message.text)

    data = await state.get_data()
    bot_message = data['bot_message']

    await bot_message.delete()

    bot_message = await message.answer(
        text='Відправте карту магазину фотографією',
        reply_markup=cancel_fsm_button
    )

    await state.update_data(bot_message=bot_message)

    await state.set_state(ShopCardStates.waiting_shop_card)


@router.message(StateFilter(ShopCardStates.waiting_shop_card), F.photo)
async def waiting_shop_card(message: Message, state: FSMContext):
    await message.delete()

    await state.update_data(photo=message.photo)

    data = await state.get_data()
    shop_name = data['shop_name']
    bot_message = data['bot_message']

    await bot_message.delete()

    await message.answer(
        text='Картку додано',
        reply_markup=view_my_cards_button
    )

    add_shop_card(message.from_user.id, shop_name, message.photo[-1].file_id)

    await state.clear()


@router.message(StateFilter(ShopCardStates))
async def delete_wrong_type(message: Message, state: FSMContext):
    await message.delete()
