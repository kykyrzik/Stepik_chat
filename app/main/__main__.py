import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage

from app.core.settings import load_setting, Settings
from app.main.dependency import setup_dependency
from app.core.loader import load_storage
from app.core.logger import log
from app.routers import (help_router,
                         send_router,
                         delete_router,
                         shit_router,
                         add_router,
                         cancel_router,
                         show_router
                         )


async def main() -> None:
    settings: Settings = load_setting()
    setup_dependency(settings)
    storage: BaseStorage = await load_storage()  # type: ignore
    dp = Dispatcher(storage=storage)
    dp.include_routers(cancel_router, delete_router, add_router,
                       shit_router, help_router, send_router,
                       show_router)

    bot: Bot = Bot(settings.bot_setting.token, parse_mode=load_setting().bot_setting.parse_mode)
    log.info("Start pooling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
