from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from aiogram.types import Message

help_router = Router()


@help_router.message(Command('help'),
                     StateFilter(None))
async def help_message(message: Message):
    await message.answer("Чтобы добавить новую фотку, введите /add_photo \n"
                         "Для того, чтобы увидеть как я сделан, введите /shit \n"
                         "Чтобы удалить триггер введите /delete_photo &ltтриггер&gt")
