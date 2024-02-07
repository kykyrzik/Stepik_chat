from typing import Annotated, AsyncGenerator, AsyncContextManager

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends
from sqlalchemy import text

from app.database.repr.media.media import MediaRepr
from app.filter.arch_message import ArchFilter
from app.database.core.gateway import DatabaseGateway
from app.common.marker.gateway import TransactionGateway

# TODO:
#  add id chat on the message.reply_animation
#  Use Redis to store id photo
#  get trigger and insert in repository.read("trigger")

router = Router(name=__name__)


@router.message(ArchFilter(),
                F.content_type.in_({'text'}))
@inject
async def arch_message(message: Message,
                       gateway: Annotated[AsyncContextManager, Depends(TransactionGateway)]):

    repository: MediaRepr = (await gateway.__aenter__()).media()
    url = (await repository.get_url("arch")).url
    image_from_pc = FSInputFile(url)
    await message.answer_photo(image_from_pc)
