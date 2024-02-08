from typing import Annotated, AsyncGenerator, AsyncContextManager

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends
from sqlalchemy import text

from app.database.repr.media.media import MediaRepr
from app.filter.filter_message import TriggerFilter
from app.common.marker.gateway import TransactionGateway

# TODO:
#  add id chat on the message.reply_animation
#  Use Redis to store id photo

router = Router(name=__name__)


@router.message(TriggerFilter(),
                F.content_type.in_({'text'}))
@inject
async def arch_message(message: Message,
                       trigger: str,
                       gateway: Annotated[AsyncContextManager, Depends(TransactionGateway)]):

    repository: MediaRepr = (await gateway.__aenter__()).media()
    url = (await repository.get_url(trigger)).url
    image_from_pc = FSInputFile(url)
    await message.answer_photo(image_from_pc)
