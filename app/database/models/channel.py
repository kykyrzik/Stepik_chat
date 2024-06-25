from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT, ForeignKey

from app.database.models.base import Base

if TYPE_CHECKING:
    from .media import Media


class Channel(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"))

    media: list[Media] = relationship(back_populates="channel")
