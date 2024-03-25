from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from aiogram.types import Message

shit_router = Router()


@shit_router.message(Command("shit"),
                     StateFilter(None))
async def help_message(message: Message):
    await message.answer("Это я https://github.com/kykyrzik/Stepik_chat")
