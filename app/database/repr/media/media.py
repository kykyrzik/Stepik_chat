from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repr.crud import BaseCRUD
from app.database.models.media import Media


class MediaRepr(BaseCRUD[AsyncSession, Media]):
    model: Type[Media] = Media
