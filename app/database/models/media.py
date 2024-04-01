from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT

from app.database.models.base import Base


class Media(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    name: Mapped[str]
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
