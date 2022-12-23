from contextlib import AbstractContextManager
from typing import Callable
from .models import User 
from sqlalchemy.orm import Session

from core.words.models import FavoriteWord


class WordService:
    def __init__(
        self, 
        session:Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        with self.session() as db:
            return db.query(User).all()

    async def get_user(self, id) -> User:
        with self.session() as db:
            user:User = (
                db
                .query(User)
                .where(User.id==id)
                .one()
            )

            return user

    async def create_user(
        self, 
        username,
        email,
        tg_id,
    ) -> User:
        
        user = User(
            username=username,
            email=email,
            tg_id=tg_id,
        )
        with self.session() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    async def update_user(self, user:User) -> User:
        with self.session() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
