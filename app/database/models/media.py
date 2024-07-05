from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT

from app.database.models.base import Base

if TYPE_CHECKING:
    from .channel import Channel


class Media(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=True)

    channel: Channel = relationship(back_populates="media")
