from typing import Annotated, AsyncContextManager
from pathlib import Path

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from fast_depends import inject, Depends

from app.database.core.gateway import DatabaseGateway
from app.common.marker.gateway import TransactionGatewayMarker


add_router = Router(name=__name__)
PATH_TO_FOLDER_PHOTO = str(Path(__file__).parent.parent.parent) + "/photo"

# TODO:
# 1. add message. if not admin. output message "add photo must only admin"


@add_router.message(Command("add", prefix="/"),
                F.content_type.in_({'text'}))
@inject
async def entry_photo(message: Message,
                      bot: Bot,
                      gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                      ):
    await message.answer(text="Entry photo")
    path_photo = f"{PATH_TO_FOLDER_PHOTO}/{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1],
                       destination=path_photo
                       )
    image_from_url = FSInputFile(path_photo)
    result = await message.answer_photo(image_from_url)
    # await message.answer_photo()
    # repository: MediaRepr = (await gateway.__aenter__()).media()
    # (await repository.create()