from typing import Type, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Media
from app.database.repr.crud import BaseCRUD
from app.database.models.media import Media


class MediaRepr(BaseCRUD[AsyncSession, Media]):
    model: Type[Media] = Media

    async def get_url(self, value: int) -> Optional[Media]:
        return await self.read(self.model.id == value)

    async def get_all_trigger_this_chat(self, value: int) -> Optional[Sequence[Media]]:
        stmt = (select(self.model).where(self.model.chat_id == value))
        return (await self._session.execute(stmt)).scalars().all()

    async def delete_media(self, value: str) -> bool:
        return await self.delete(self.model.name == value)

    async def check_url