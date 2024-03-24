import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from fast_depends import dependency_provider

from app.core.settings import load_setting
from app.routers.start_add_photo import add_router
from app.routers.send_photo import send_router
from app.database.core.session import (create_engine,
                                       create_as_session_maker
                                       )
from app.common.marker.gateway import TransactionGatewayMarker
from app.common.marker.redis import redis_marker
from app.database.core.gateway import TransactionGateway
from app.database.redis.connection import get_connection_pool, GetRedisConnection
from app.core.loader import load_storage


# noinspection PyArgumentList
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    setting = load_setting()
    engine = create_engine(setting.db_setting.get_url)
    async_session_maker = create_as_session_maker(engine)
    redis_pool = await get_connection_pool(setting.redis_settings.get_url)
    dependency_provider.override(redis_marker, GetRedisConnection(redis_pool))
    dependency_provider.override(TransactionGatewayMarker, TransactionGateway(async_session_maker()))
    storage = await load_storage()
    dp = Dispatcher(storage=storage)
    # middleware = FilterCommandMiddleware()

    # router.message.outer_middleware.register(middleware)
    dp.include_router(add_router)
    dp.include_router(send_router)

    bot: Bot = Bot(setting.bot_setting.token, parse_mode=load_setting().bot_setting.parse_mode)
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
