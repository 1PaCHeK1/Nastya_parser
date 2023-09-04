from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import User, Post, ViewedPost


class PostRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_unread_post(self, user: User) -> Sequence[Post]:
        subquery = (
            select(Post.id)
            .except_(
                select(ViewedPost.post_id)
                .where(ViewedPost.user_id == user.id)
                .with_only_columns(ViewedPost.post_id)
            )
            .subquery()
        )

        stmt = select(Post).join(subquery, Post.id == subquery.c.id).order_by(Post.id)

        return self.session.scalars(stmt).all()
