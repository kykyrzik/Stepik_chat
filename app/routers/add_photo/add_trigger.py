from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter

from .start_add_photo import add_router
from .state import AddPhotoState


@add_router.message(StateFilter(AddPhotoState.add_trigger))
async def add_trigger(message: Message, state: FSMContext):
    print("add trigger")
    trigger_word = message.text
    await state.update_data(trigger=trigger_word)
    await message.answer(text=f"""хорошо, вы установили {trigger_word}.
                                  Теперь хотелось бы увидеть фотографию.
                                  Отправьте же мне ее""")
    await state.set_state(AddPhotoState.add_photo)