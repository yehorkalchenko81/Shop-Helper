from aiogram.filters.command import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router

from database import add_new_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.delete()

    add_new_user(message.from_user.id, message.from_user.full_name)

    await message.answer(
        text='Відправ мені список одним повідомленням!',
        reply_markup=ReplyKeyboardRemove()
    )
