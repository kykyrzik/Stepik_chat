import os
from typing import Annotated

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from aiogram.types import Message
from fast_depends import inject, Depends

from app.common.marker.gateway import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway

delete_router = Router()


@delete_router.message(Command('delete_photo'),
                       StateFilter(None))
@inject
async def help_message(message: Message,
                       gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)]
                       ):
    media_repr = gateway.media()
    trigger = message.text[14:]
    path: str = (await media_repr.get_url(trigger)).url
    if path:
        os.remove(path)
        await media_repr.delete_media(trigger)
        await message.answer(f"Вы удалили слово {trigger}")
    else:
        await message.answer("Такого слова в базе нет")
