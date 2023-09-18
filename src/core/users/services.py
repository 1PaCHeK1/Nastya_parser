from datetime import UTC, datetime
from typing import overload
from .schemas import RegistrationToken

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.users.schemas import (
    UserCreateSchema,
    UserRegistrationApiDto,
    UserRegistrationTgDto,
    UserSchema,
    UserUpdateSchema,
)
from db.models import User


class UserTgService:
    def __init__(self, session: Session):
        self._session = session
    
    async def get_users(self) -> list[UserSchema]:
        return list(map(UserSchema.from_orm, self._session.scalars(select(User))))

    async def get_user(self, id: int) -> UserSchema:
        user = self._session.scalar(select(User).where(User.id == id))
        return UserSchema.from_orm(user)

    async def get_user_by_tg_id(self, tg_id: int) -> UserSchema | None:
        user = self._session.scalar(select(User).where(User.tg_id == tg_id))
        if user is not None:
            return UserSchema.from_orm(user)

    async def check_user(self, tg_id: int) -> bool:
        return bool(self._session.scalar(select(User.id).where(User.tg_id == tg_id)))

    async def create_user(
        self,
        user: UserCreateSchema,
    ) -> UserSchema:
        user = User(**user.dict())
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return UserSchema.from_orm(user)

    async def update_user(self, user: UserUpdateSchema) -> UserSchema:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return UserSchema.from_orm(user)


class HashService:
    def encode_password(self, password: str) -> str:
        return bcrypt.hashpw(
            password.encode(),
            salt=bcrypt.gensalt(
                rounds=12,
                prefix=b"2b",
            ),
        ).decode()

    def check_password(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode(),
        )

    def encode_user(self, user: User) -> str:
        return jwt.encode(
            {
                "id": user.id,
                "create_at": user.create_at.isoformat(),
            },
            key="test",
        )

    def decode_user(self, token: str) -> RegistrationToken:
        return RegistrationToken.parse_obj(
            jwt.decode(token, key="test", algorithms=["HS256"]),
        )


class UserService:
    def __init__(
        self,
        session: Session,
        hash: HashService,
    ) -> None:
        self._session = session
        self._hash = hash

    def email_exists(self, email: str) -> bool:
        stmt = select(User.id).where(User.email == email)
        stmt_exists = select(stmt.exists())
        return self._session.scalars(stmt_exists).one()

    @overload
    def registration(self, dto: UserRegistrationApiDto) -> User:
        ...

    @overload
    def registration(self, dto: UserRegistrationTgDto) -> User:
        ...

    def registration(self, dto: UserRegistrationApiDto | UserRegistrationTgDto) -> User:
        if isinstance(dto, UserRegistrationApiDto):
            return self._registration_from_api(dto)
        if isinstance(dto, UserRegistrationTgDto):
            return self._registration_from_tg(dto)

    def _registration_from_api(self, dto: UserRegistrationApiDto) -> User:
        user = User(
            username=dto.username,
            email=dto.email,
        )
        user.create_at = datetime.now(tz=UTC).date()
        user.password = self._hash.encode_password(dto.password)
        self._session.add(user)
        return user

    def _registration_from_tg(dto: UserRegistrationTgDto) -> User:
        raise NotImplementedError

    def flush(self) -> None:
        self._session.flush()
