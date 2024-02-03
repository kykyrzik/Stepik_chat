from app.database.core.unit_of_work import SQLAlchemyUnitOfWork
from app.database.repr.media.media import MediaRepr


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


def database_gateway_factory(unit_of_work) -> DatabaseGateway:
    return DatabaseGateway(unit_of_work)
