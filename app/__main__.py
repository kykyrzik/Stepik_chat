import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from fast_depends import dependency_provider

from app.core.settings import load_setting
from app.routers.send_photo import router
from app.routers.add_photo import add_router
from app.database.core.session import (create_engine,
                                       create_as_session_maker
                                       )
from app.common.marker.gateway import TransactionGateway
from app.common.marker.redis import RedisMarker
from app.database.core.gateway import transaction_gateway
from app.database.redis.connection import get_connection_pool, get_redis_connection


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    setting = load_setting()
    engine = create_engine(setting.db_setting.get_url)
    async_session_maker = create_as_session_maker(engine)
    redis_pool = get_connection_pool(setting.redis_settings.get_url)
    dependency_provider.override(RedisMarker, lambda: get_redis_connection(redis_pool))  # type: ignore
    dependency_provider.override(TransactionGateway, lambda: transaction_gateway(async_session_maker()))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(add_router)
    bot: Bot = Bot(setting.bot_setting.token, parse_mode=load_setting().bot_setting.parse_mode)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
