from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from datetime import datetime

from logger import logger
from database import add_new_user
from keyboards import start_menu_keyboard

router = Router()


@router.message(StateFilter(None), Command(commands=['start', 'menu']))
async def start_menu_cammand(message: Message):
    await message.delete()

    add_new_user(message.from_user.id, message.from_user.full_name)

    await message.answer(
        text='Меню бота:',
        reply_markup=start_menu_keyboard
    )

    logger(f'{"-" * 25}\n'
           f'Func: start_menu_cammand\n'
           f'User_id: {message.from_user.id}\n'
           f'User_name: {message.from_user.full_name}\n'
           f'Time: {datetime.now()}\n'
           )


@router.callback_query(F.data == 'start_menu')
async def start_menu_call_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        text='Меню бота:',
        reply_markup=start_menu_keyboard
    )

    logger(f'{"-" * 25}\n'
           f'Func: start_menu_call_back\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Time: {datetime.now()}\n'
           )

