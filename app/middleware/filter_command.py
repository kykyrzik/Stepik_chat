from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import TelegramObject


class FilterCommandMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                 ) -> Any:
        if not isinstance(event, Message):
            await handler(event, data)
        if not event.text.startswith("/"):
            await handler(event, data)
        return None
