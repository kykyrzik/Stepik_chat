import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from app.core.settings import load_setting
from app.routers.arch_message import router

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot: Bot = Bot(load_setting().bot_setting.token, parse_mode=load_setting().bot_setting.parse_mode)
    await dp.start_polling(bot)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
