from typing import Annotated

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage

from fast_depends import Depends, inject
from redis.asyncio import Redis

from app.common.marker.redis import redis_marker


@inject
async def load_storage(client: Annotated[Redis, Depends(redis_marker)]) -> BaseStorage:
    try:
        from aiogram.fsm.storage.redis import RedisStorage

        storage = RedisStorage(redis=client)
    except ImportError:
        from aiogram.fsm.storage.memory import MemoryStorage

        storage = MemoryStorage()  # type: ignore

    return storage


async def load_admins(bot: Bot, chat_id: int) -> set[int]:
    admins = await bot.get_chat_administrators(chat_id)
    return {admin.user.id for admin in admins}
