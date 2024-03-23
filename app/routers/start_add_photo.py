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

PATH_TO_FOLDER_PHOTO = str(Path(__file__).parent.parent) + "/photos"

add_router = Router(name=__name__)

# TODO:
# 1. add message. if not admin. output message "add photo must only admin"
# 2. simple user: if not start user


@add_router.message(Command("add", prefix="/"),
                    StateFilter(default_state)
                    )
async def entry_photo(message: Message, state: FSMContext):
    print("entry")
    await message.answer(text="""Начнём же добавлять.
     Введите слово, на которое будет реагировать бот""")
    await state.set_state(AddPhotoState.add_trigger)


@add_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний')
    await state.clear()


@add_router.message(StateFilter(AddPhotoState.add_trigger))
async def add_trigger(message: Message, state: FSMContext):
    print("add trigger")
    trigger_word = message.text
    await state.update_data(trigger=trigger_word)
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
                       destination=PATH_TO_FOLDER_PHOTO
                       )
    image_from_url = FSInputFile(path_photo)
    await state.update_data(url=image_from_url.path)
    print(state.storage)


