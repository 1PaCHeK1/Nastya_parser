from contextlib import AbstractContextManager
from typing import Callable
from core.users.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from .models import User 
from core.words.models import FavoriteWord


class UserService:
    def __init__(self, session:Callable[..., AbstractContextManager[Session]]) -> None:
        self.session = session

    async def get_users(self) -> list[UserSchema]:
        with self.session() as db:
            return list(map(UserSchema.from_orm, db.query(User).all()))
    
    async def get_user(self, id) -> UserSchema:
        with self.session() as db:
            user = (
                db
                .query(User)
                .where(User.id==id)
                .one()
            )
            return UserSchema.from_orm(user)

    async def get_user_by_tg_id(self, tg_id) -> UserSchema|None:
        with self.session() as db:
            user = (
                db
                .query(User)
                .where(User.tg_id==tg_id)
                .first()
            )
        if user is not None:
            return UserSchema.from_orm(user)
    
    async def check_user(self, tg_id:int):
        with self.session() as db:
            return bool(db.query(User.id).where(User.tg_id==tg_id).scalar())

    async def create_user(
        self, 
        user: UserCreateSchema
    ) -> UserSchema:

        user = User(**user.dict())
        with self.session() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return UserSchema.from_orm(user)

    async def update_user(self, user:UserUpdateSchema) -> UserSchema:
        with self.session() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return UserSchema.from_orm(user)
