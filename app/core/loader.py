from typing import Annotated

from aiogram import Bot
from aiogram.fsm import storage as aiogram_storage


from fast_depends import Depends, inject
from redis.asyncio import Redis

from app.common.marker import RedisMarker


@inject
async def load_storage(client: Annotated[Redis, Depends(RedisMarker)]) -> aiogram_storage.base.BaseStorage:
    try:
        storage = aiogram_storage.redis.RedisStorage(redis=client)
    except ImportError:
        storage = aiogram_storage.redis.MemoryStorage()
    return storage


async def load_admins(bot: Bot, chat_id: int) -> set[int]:
    admins = await bot.get_chat_administrators(chat_id)
    return {admin.user.id for admin in admins}
