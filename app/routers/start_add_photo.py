from pathlib import Path
from typing import Annotated

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from fast_depends import inject, Depends

from app.fsm.add_photo_state import AddPhotoState
from app.common.marker.gateway import TransactionGatewayMarker
from app.database.core.gateway import DatabaseGateway
from app.core.settings import PATH_TO_HOME

PATH_TO_FOLDER_PHOTO = str(PATH_TO_HOME) + "/media"

add_router = Router(name=__name__)

# TODO:
# 1. add message. if not admin. output message "add photo must only admin"
# 2. simple user: if not start user


@add_router.message(Command("add", prefix="/"),
                    StateFilter(default_state)
                    )
async def entry_photo(message: Message, state: FSMContext):
    await message.answer(text="""Начнём же добавлять.
     Введите слово, на которое будет реагировать бот
     если вы хоитите выйти введите /cancel""")
    await state.set_state(AddPhotoState.add_trigger)


@add_router.message(StateFilter(AddPhotoState.add_trigger))
async def add_trigger(message: Message, state: FSMContext):
    trigger_word = message.text
    await state.update_data(name=trigger_word)
    await message.answer(text=f"""хорошо, вы установили {trigger_word}.
                                  Теперь хотелось бы увидеть фотографию.
                                  Отправьте же мне ее""")
    await state.set_state(AddPhotoState.add_photo)


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
    await state.update_data(url=image_from_url.path)
    data = await state.get_data()
    media_repr = gateway.media()
    await media_repr.create(**data)
    await message.answer(text='Фото успешно добавленно')
    await state.clear()


@add_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний')
    await state.clear()


