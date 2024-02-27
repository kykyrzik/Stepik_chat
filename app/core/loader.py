from typing import Annotated

from aiogram.fsm.storage.base import BaseStorage

from fast_depends import Depends, inject
from redis.asyncio import Redis

from app.common.marker.redis import redis_marker


@inject
async def load_storage(client: Annotated[Redis, Depends(redis_marker)]):
    try:
        from aiogram.fsm.storage.redis import RedisStorage

        storage = RedisStorage(redis=client)
    except ImportError:
        from aiogram.fsm.storage.memory import MemoryStorage

        storage = MemoryStorage()  # type: ignore

    return storage
