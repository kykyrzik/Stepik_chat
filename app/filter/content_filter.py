from typing import Optional

from aiogram.types import Message


class ContentFilter:
    async def __call__(self, message: Message) -> Optional[str]:
        return check_type(message.content_type)


def check_type(content_type: str) -> Optional[str]:
    for i in ("photo", "video", "audio", "voice", "sticker"):
        if i == content_type:
            return i
