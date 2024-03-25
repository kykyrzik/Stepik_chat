from typing import Union, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.repr.crud import BaseCRUD
from app.database.models.media import Media


class MediaRepr(BaseCRUD[AsyncSession, Media]):
    model: Type[Media] = Media

    async def get_url(self, field: str) -> Union[Media, None]:
        return await self.read(self.model.name == field)

    async def get_all_trigger(self) -> Union[list[str], list]:
        stmt = select(self.model.name)
        return (await self._session.execute(stmt)).scalars().all()  # type: ignore
