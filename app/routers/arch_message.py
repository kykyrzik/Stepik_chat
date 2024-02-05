from typing import Annotated

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends, dependency_provider

from app.filter.arch_message import ArchFilter
from app.database.core.gateway import DatabaseGateway
from app.common.marker.gateway import TransactionGateway
from app.database.core.session import get_session

# TODO:
#  add id chat on the message.reply_animation
#  Use Redis to store id photo
#  get trigger and insert in repository.read("trigger")


router = Router(name=__name__)


@router.message(ArchFilter(),
                F.content_type.in_({'text'}))
@inject
async def arch_message(message: Message,
                       gateway=Depends(get_session)):
    repository = gateway
    # async for i in repository:
    print(repository)
    # url = repository.read("arch").url
    # image_from_pc = FSInputFile(url)
    # await message.answer_photo(image_from_pc)
