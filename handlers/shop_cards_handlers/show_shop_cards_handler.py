from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from datetime import datetime

from keyboards import set_shop_cards_keyboard
from logger import logger

router = Router()


@router.callback_query(F.data == 'view_my_cards')
async def show_card_list(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        text='Ваші картки магазинів:',
        reply_markup=set_shop_cards_keyboard(callback.from_user.id).as_markup()
    )

    logger(f'{"-" * 25}\n'
           f'Func: show_card_list\n'
           f'User_id: {callback.from_user.id}\n'
           f'User_name: {callback.from_user.full_name}\n'
           f'Time: {datetime.now()}\n'
           )
