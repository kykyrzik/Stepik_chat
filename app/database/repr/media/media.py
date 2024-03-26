from typing import Union, Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.repr.crud import BaseCRUD
from app.database.models.media import Media


class MediaRepr(BaseCRUD[AsyncSession, Media]):
    model: Type[Media] = Media

    async def get_url(self, value: str) -> Optional[Media]:
        return await self.read(self.model.name == value)

    async def get_all_trigger(self) -> Union[list[str], list]:
        stmt = select(self.model.name)
        return (await self._session.execute(stmt)).scalars().all()  # type: ignore

    async def delete_media(self, value: str) -> bool:
        return await self.delete(self.model.name == value)
