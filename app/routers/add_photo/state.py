from aiogram.fsm.state import State, StatesGroup


class AddPhotoState(StatesGroup):
    add_trigger = State()
    add_photo = State()
