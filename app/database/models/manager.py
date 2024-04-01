from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT

from app.database.models.base import Base


class Manager(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column()