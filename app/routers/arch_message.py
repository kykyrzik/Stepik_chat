from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from app.filter.arch_message import ArchFilter
# TODO: add repr
#  from app.service.repr.arch import load_url
#  add id chat on the message.reply_animation
#  Use Redis to store id photo

router = Router(name=__name__)


@router.message(ArchFilter(),
                F.content_type.in_({'text'}))
async def arch_message(message: Message):
    file_ids = []
    if file_ids:
        await message.reply_animation(message.animation.file_id)
    else:
        image_from_pc = FSInputFile(r".\photo\photo_2024-01-10_23-01-47.jpg")
        result = await message.answer_photo(image_from_pc)
        file_ids.append(result.photo[-1].file_id)

