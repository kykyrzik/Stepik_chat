from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.core.unit_of_work import SQLAlchemyUnitOfWork
from app.database.repr.media.media import MediaRepr
from app.database.core.unit_of_work import factory_unit_of_work


class DatabaseGateway:
    def __init__(self, uow: SQLAlchemyUnitOfWork):
        self.uow = uow

    async def __aenter__(self):
        await self.uow.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.uow.__aexit__(exc_type, exc_val, exc_tb)

    def media(self) -> MediaRepr:
        return MediaRepr(self.uow.session)


def database_gateway_factory(unit_of_work: SQLAlchemyUnitOfWork) -> DatabaseGateway:
    return DatabaseGateway(unit_of_work)


async def setup_transaction_gateway(self) -> AsyncIterable[DatabaseGateway]:
    async with database_gateway_factory(factory_unit_of_work(self.session)) as gateway:
        yield gateway
