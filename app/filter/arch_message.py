from dataclasses import dataclass

from aiogram.types import Message
from aiogram.filters import BaseFilter

from app.config.arch_trigger import ARCH_WORDS


@dataclass
class ArchFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await check(message)


async def check(message: Message) -> bool:
    for trigger in ARCH_WORDS:
        if trigger in message.text:
            return trigger
