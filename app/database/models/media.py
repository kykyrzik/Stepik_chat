from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Media(Base):
    id: Mapped[int] = mapped_column(index=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
