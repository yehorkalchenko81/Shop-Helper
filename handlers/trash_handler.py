from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def delete_trash_message(message: Message):
    await message.delete()
