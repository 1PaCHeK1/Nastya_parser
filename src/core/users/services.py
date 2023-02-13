from core.users.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from sqlalchemy.orm import Session
from .models import User


class UserService:
    async def get_users(self, session: Session) -> list[UserSchema]:
        return list(map(UserSchema.from_orm, session.query(User).all()))

    async def get_user(self, id, session: Session) -> UserSchema:
        user = (
            session
            .query(User)
            .where(User.id==id)
            .one()
        )
        return UserSchema.from_orm(user)

    async def get_user_by_tg_id(self, tg_id: int, session: Session) -> UserSchema|None:
        user = (
            session
            .query(User)
            .where(User.tg_id==tg_id)
            .first()
        )
        if user is not None:
            return UserSchema.from_orm(user)

    async def check_user(self, tg_id:int, session: Session):
        return bool(session.query(User.id).where(User.tg_id==tg_id).scalar())

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
