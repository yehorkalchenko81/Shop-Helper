from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database import read_shop_cards, remove_shop_cards
from states import ConfirmDeleteState
from keyboards import confirmating_keyboard, view_my_cards_button

router = Router()


@router.callback_query(F.data.contains('viewcard_'))
async def show_card(callback: CallbackQuery):
    _, shop_name = callback.data.split('_')

    raw_data = read_shop_cards(callback.from_user.id)
    shop_card, *_ = [row[1] for row in raw_data if shop_name in row]

    await callback.message.delete()

    await callback.message.answer_photo(photo=shop_card)


@router.callback_query(StateFilter(None), F.data.contains('delcard_'))
async def delete_card(callback: CallbackQuery, state: FSMContext):
    _, shop_name = callback.data.split('_')

    raw_data = read_shop_cards(callback.from_user.id)
    shop_card, *_ = [row[0] for row in raw_data if shop_name in row]

    # await callback.message.delete()

    await callback.message.edit_text(
        text=f'Ви впевнені, що хочете видалити карту магазину {shop_name}',
        reply_markup=confirmating_keyboard
    )

    await state.update_data(shop_name=shop_name, user_id=callback.from_user.id)

    await state.set_state(ConfirmDeleteState.waiting_confirmation)


@router.callback_query(StateFilter(ConfirmDeleteState.waiting_confirmation))
async def collect_chose(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    shop_name = data['shop_name']
    if callback.data == 'deleting_confirmed':
        user_id = data['user_id']

        remove_shop_cards(user_id, shop_name)

        await callback.message.delete()

        await callback.message.answer(
            text=f'Ви видалити карту магазину {shop_name}',
            reply_markup=view_my_cards_button
        )

        await state.clear()
    else:
        await callback.message.delete()
        await callback.message.answer(
            text=f'Ви відмінили видалення картки магазину {shop_name}',
            reply_markup=view_my_cards_button
        )
