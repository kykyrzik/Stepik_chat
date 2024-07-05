from typing import Annotated

from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from fast_depends import inject, Depends

from app.fsm.add_photo_state import AddPhotoState
from app.common.marker import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway
from app.filter import IsAdmin, ContentFilter
from app.core.settings import PATH_TO_HOME

PATH_TO_FOLDER_PHOTO = str(PATH_TO_HOME) + "/media"

add_router = Router(name=__name__)


@add_router.message(Command("add"),
                    IsAdmin(),
                    StateFilter(default_state)
                    )
async def entry_photo(message: Message,
                      state: FSMContext):
    await message.answer(text="""Начнём же добавлять. Введите слово, на которое будет реагировать бот\nВведите /stop, чтобы остановить процесс добавления медиа""")
    await state.set_state(AddPhotoState.add_trigger)


@add_router.message(F.text, StateFilter(AddPhotoState.add_trigger))
@inject
async def add_trigger(message: Message,
                      state: FSMContext,
                      gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)]
                      ):
    media_repr = gateway.media()
    trigger_word = message.text
    media_exists = await media_repr.get_url(trigger_word, message.chat.chat_id)
    if media_exists:
        await message.answer(f"Слово {trigger_word} уже занято")
    else:
        await state.update_data(name=trigger_word)
        await message.answer(text=f"""Хорошо, вы установили {trigger_word}.\nТеперь хотелось бы увидеть медиа.\nОтправьте же мне ее""")
        await state.set_state(AddPhotoState.add_media)


@add_router.message(ContentFilter, StateFilter(AddPhotoState.add_media))
@inject
async def add_photo(message: Message,
                    trigger_type: str,
                    gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
                    state: FSMContext):

    if trigger_type == "photo":
        media_id = message.photo.id
    elif trigger_type == "audio":
        media_id = message.audio.file_id
    elif trigger_type == "video":
        media_id = message.video.file_id
    elif trigger_type == "voice":
        media_id = message.voice.file_id
    else:
        media_id = message.sticker.file_id

    await state.update_data(media_id=media_id)
    data = await state.get_data()
    media_repr = gateway.media()
    await media_repr.create(**data)
    await message.answer(text='Фото успешно добавленно')
    await state.clear()
