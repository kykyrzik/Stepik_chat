from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Media(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
