from dataclasses import dataclass
from re import search

from aiogram.types import Message
from aiogram.filters import BaseFilter

from app.config.arch_trigger import ARCH_WORDS


@dataclass
class TriggerFilter(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str]:
        return await check(message)


async def check(message: Message) -> dict[str, str]:
    for trigger_key in ARCH_WORDS:
        pattern = f'{trigger_key}'
        if search(pattern, message.text):
            return {"trigger": trigger_key}
