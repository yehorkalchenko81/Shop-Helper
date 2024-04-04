from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import set_shop_cards_keyboard

router = Router()


@router.message(Command(commands=['shop_cards']))
@router.message(F.text == 'Переглянути мої картки')
async def show_card_list(message: Message):
    await message.delete()

    await message.answer(
        text='Ваші картки магазинів:',
        reply_markup=set_shop_cards_keyboard(message.from_user.id).as_markup()
    )
