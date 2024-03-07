from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .state import AddPhotoState


add_router = Router(name=__name__)

# TODO:
# 1. add message. if not admin. output message "add photo must only admin"
# 2. simple user: if not start user


@add_router.message(Command("add", prefix="/"),
                    StateFilter(None)
                    )
async def entry_photo(message: Message, state: FSMContext):
    print("entry")
    await message.answer(text="""Начнём же добавлять.
     Введите слово, на которое будет реагировать бот""")
    await state.set_state(AddPhotoState.add_trigger)
