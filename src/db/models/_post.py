from __future__ import annotations
from datetime import datetime

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from db.base import Base
from db.types import int_pk, text

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class PostTags(Base):
    __tablename__ = "posttags"

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int_pk]

    title: Mapped[str]
    body: Mapped[text]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    is_publish: Mapped[bool]
    publish_date: Mapped[datetime]

    tags: Mapped[list[Tag]] = relationship(
        secondary="posttags",
        back_populates="posts",
    )


class ViewedPost(Base):
    __tablename__ = "viewedpost"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int_pk]

    name: Mapped[str]
    rating: Mapped[int]

    posts: Mapped[list[Post]] = relationship(
        secondary="posttags",
        back_populates="tags",
    )
