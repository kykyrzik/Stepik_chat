from typing import TypeVar, Callable

from fast_depends import dependency_provider

from app.core.logger import log
from app.common.marker import TransactionGatewayMarker, RedisMarker
from app.core.settings import Settings
from app.database.core.gateway import setup_transaction_gateway
from app.database.redis.connection import get_connection_pool
from app.database.core.session import (create_engine,
                                       create_as_session_maker
                                       )


DependencyType = TypeVar("DependencyType")


def singleton(value: DependencyType) -> Callable[[], DependencyType]:
    def singleton_factory() -> DependencyType:
        return value
    return singleton_factory


def setup_dependency(settings: Settings) -> None:
    engine = create_engine(settings.db_setting.get_url)
    async_session_maker = create_as_session_maker(engine)
    transaction_gateway = setup_transaction_gateway(async_session_maker)
    log.info("Connection to db success")

    redis_pool = get_connection_pool(settings.redis_settings.get_url)
    log.info("Connection to redis success")

    dependency_provider.override(RedisMarker, singleton(redis_pool))
    dependency_provider.override(TransactionGatewayMarker, singleton(transaction_gateway))
