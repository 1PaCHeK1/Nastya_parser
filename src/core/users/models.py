from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import date
from sqlalchemy.orm import relationship, mapped_column, Mapped

from core.database import Base
from core.database.types import str_128, int_pk

if TYPE_CHECKING:
    from core.words.models import Word


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str_128|None]
    email: Mapped[str_128|None] = mapped_column(unique=True)
    tg_id: Mapped[int|None] = mapped_column(unique=True)
    create_at: Mapped[date] = mapped_column(insert_default=date.today)
    is_active: Mapped[bool] = mapped_column(insert_default=False)

    favorite_words: Mapped[list[Word]] = relationship(
        secondary="favoriteword",
        back_populates="favorite_for_users",
    )
