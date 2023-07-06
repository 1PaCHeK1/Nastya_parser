from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.base import Base

if TYPE_CHECKING:
    from db.models import User


class Token(Base):
    __tablename__ = "tokens"

    token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    user: Mapped[User] = relationship()
