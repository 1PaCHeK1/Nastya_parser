from contextlib import AbstractContextManager
from typing import Callable
from core.users.schemas import UserCreate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from .models import User 
from core.words.models import FavoriteWord


class UserService:
    def __init__(self, session:Callable[..., AbstractContextManager[Session]]) -> None:
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

    async def check_user(self, tg_id:int):
        with self.session() as db:
            return bool(db.query(User.id).where(User.tg_id==tg_id).scalar())

    async def create_user(
        self, 
        user: UserCreate
    ) -> User:
        
        user = User(**user.dict())
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
