from typing import Annotated

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from aiogram.types import Message
from fast_depends import inject, Depends

from app.common.marker.gateway import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway
from app.filter.is_admin import IsAdmin
from app.filter.throttling import ThrottlingFilter
from app.lexicon.text_builders import section_builder

show_router = Router()


@show_router.message(Command('show'),
                     IsAdmin(),
                     ThrottlingFilter(rate=5),
                     StateFilter(None)
                     )
@inject
async def help_message(message: Message,
                       gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)]
                       ):
    media_repr = gateway.media()
    all_trigger = await media_repr.get_all_trigger()
    await message.answer(**section_builder("Вот все триггеры:", all_trigger))
