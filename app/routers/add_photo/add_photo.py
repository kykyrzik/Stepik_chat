from typing import Annotated
from pathlib import Path

from aiogram.filters import StateFilter
from fast_depends import inject, Depends
from aiogram import F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from app.database.core.gateway import DatabaseGateway
from app.common.marker.gateway import TransactionGatewayMarker
from .start_add_photo import add_router
from .state import AddPhotoState

PATH_TO_FOLDER_PHOTO = str(Path(__file__).parent.parent.parent) + "/photo"


@add_router.message(StateFilter(AddPhotoState.add_photo))
@inject
async def add_photo(message: Message,
                    bot: Bot,
                    gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                    state: FSMContext):
    path_photo = f"{PATH_TO_FOLDER_PHOTO}/{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1],
                       destination=path_photo
                       )
    image_from_url = FSInputFile(path_photo)
    await state.update_data(url=image_from_url)
    print(state.storage)
    # await message.answer_photo()
    # repository: MediaRepr = (await gateway.__aenter__()).media()
    # (await repository.create()
