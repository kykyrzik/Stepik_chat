from pathlib import Path
from functools import lru_cache

from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict


PATH_TO_HOME = Path(__name__).parent.parent.parent


class DBSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{PATH_TO_HOME}/.env',
                                      env_prefix='DB_',
                                      case_sensitive=False)
    user: str
    port: int
    host: str
    password: str
    name: str
    uri: str

    @property
    def get_url(self) -> str:
        return self.uri.format(self.user,
                               self.password,
                               self.host,
                               self.port,
                               self.name,
                               )


class BotSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{PATH_TO_HOME}/.env',
                                      env_prefix='BOT_',
                                      case_sensitive=False)
    token: str
    parse_mode: ParseMode | str = ParseMode.HTML


class Settings(BaseSettings):
    bot_setting = BotSetting()
    db_setting = DBSetting()


@lru_cache
def load_setting() -> Settings:
    return Settings()
