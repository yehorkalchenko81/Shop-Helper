from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router

from database import add_new_user

start_router = Router()


@start_router.message(Command('strat'))
async def start(message: Message):
    add_new_user(message.from_user.id, message.from_user.full_name)

    await message.answer(
        text='Відправ мені список одним повідомленням!',
        reply_markup=ReplyKeyboardRemove()
    )
