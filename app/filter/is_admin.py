from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.core.loader import load_admins
from app.core.settings import load_setting

# TODO: maybe save admins in the cache and update before 5 minute
# TODO: refactor send settingZ


class IsAdmin(BaseFilter):
    def __init__(self):
        self.admins = None

    async def __call__(self, message: Message) -> bool:
        if not self.admins:
            self.admins = await load_admins(message.bot, load_setting().chat_settings.id)

        return message.from_user.id in self.admins
