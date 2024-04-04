from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from keyboards import set_shop_cards_keyboard

router = Router()


@router.callback_query(F.data == 'view_my_cards')
async def show_card_list(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        text='Ваші картки магазинів:',
        reply_markup=set_shop_cards_keyboard(callback.from_user.id).as_markup()
    )
