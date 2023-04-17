from core.users.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User


class UserService:
    async def get_users(self, session: Session) -> list[UserSchema]:
        return list(map(UserSchema.from_orm, session.scalars(select(User))))

    async def get_user(self, id: int, session: Session) -> UserSchema:
        user = session.scalar(
            select(User)
            .where(User.id==id)
        )
        return UserSchema.from_orm(user)

    async def get_user_by_tg_id(self, tg_id: int, session: Session) -> UserSchema|None:
        # SELECT * FROM users
        user = session.scalar(
            select(User)
            .where(User.tg_id==tg_id)
        )
        # user = (
        #     session
        #     .query(User)
        #     .where(User.tg_id==tg_id)
        #     .first()
        # )
        if user is not None:
            return UserSchema.from_orm(user)

    async def check_user(self, tg_id:int, session: Session):
        return bool(session.scalar(select(User.id).where(User.tg_id==tg_id)))

    async def create_user(
        self,
        user: UserCreateSchema,
        session: Session,
    ) -> UserSchema:
        user = User(**user.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserSchema.from_orm(user)

    async def update_user(self, user:UserUpdateSchema, session: Session) -> UserSchema:
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserSchema.from_orm(user)
