from typing import Type, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (insert,
                        select,
                        update,
                        delete)

from app.common.types import Model, SessionType
from app.common.db.base import AbstractCRUDRepository


class BaseCRUD(AbstractCRUDRepository[SessionType, Model]):

    model: Type[Model]

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, **values: Any) -> Optional[Model]:
        stmt = insert(self.model).values(**values).returning(self.model)
        return (await self._session.execute(stmt)).sclars().first()

    async def read(self, *clauses: Any) -> Optional[Model]:
        stmt = select(self.model).where(*clauses)
        return (await self._session.execute(stmt)).scalars().first()

    async def update(self,
                     *clauses: Any,
                     **values: Any
                     ) -> Optional[Model]:
        stmt = update(self.model).where(*clauses).values(**values).returning(self.model)
        return (await self._session.execute(stmt)).scalars().all()

    async def delete(self, *clauses: Any) -> bool:
        stmt = delete(self.model).where(*clauses).returning(self.model)
        return (await self._session.execute(stmt)).scalars().all()
