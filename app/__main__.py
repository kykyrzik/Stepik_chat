import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from fast_depends import dependency_provider

from app.core.settings import load_setting
from app.routers.arch_message import router
# from app.database.core.session import (create_engine,
#                                        create_as_session_maker,
#                                        )
from app.common.marker.gateway import TransactionGateway
from app.database.core.gateway import transaction_gateway


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    setting = load_setting()
    # dependency_provider.override(TransactionGateway, lambda: transaction_gateway(session_maker()))
    dp = Dispatcher()
    dp.include_router(router)
    bot: Bot = Bot(setting.bot_setting.token, parse_mode=load_setting().bot_setting.parse_mode)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
