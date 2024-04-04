from aiogram import Router
from aiogram.types import Message
from datetime import datetime

from logger import logger

router = Router()


@router.message()
async def delete_trash_message(message: Message):
    await message.delete()

    logger(f'{"-" * 25}\n'
           f'Func: delete_trash_message\n'
           f'User_id: {message.from_user.id}\n'
           f'User_name: {message.from_user.full_name}\n'
           f'User_input: {message.text}\n'
           f'Time: {datetime.now()}\n'
           )
