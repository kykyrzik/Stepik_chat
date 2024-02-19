from pathlib import Path
from functools import lru_cache

from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict


PATH_TO_HOME = Path(__file__).parent.parent.parent


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
        return self.uri.format(user=self.user,
                               password=self.password,
                               host=self.host,
                               port=self.port,
                               name=self.name
                               )


class BotSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{PATH_TO_HOME}/.env',
                                      env_prefix='BOT_',
                                      case_sensitive=False)
    token: str
    parse_mode: ParseMode | str = ParseMode.HTML


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{PATH_TO_HOME}/.env",
        case_sensitive=False,
        env_prefix="REDIS_",
    )
    host: str
    port: int
    uri: str

    @property
    def get_url(self) -> str:
        return self.uri.format(host=self.host,
                               port=self.port)



class Settings(BaseSettings):
    bot_setting: BotSetting = BotSetting()
    db_setting: DBSetting = DBSetting()
    redis_settings: RedisSettings = RedisSettings()

@lru_cache
def load_setting() -> Settings:
    return Settings()
