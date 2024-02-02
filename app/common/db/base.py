import abc
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.types import Model, SessionType


class AbstractCRUDRepository(abc.ABC,
                             typing.Generic[SessionType, Model]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def create(self, **values: typing.Any) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def read(self, *clauses: typing.Any) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self,
                     *clauses: typing.Any,
                     **values: typing.Any
                     ) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: typing.Any) -> typing.Any:
        raise NotImplementedError

