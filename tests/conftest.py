from collections.abc import AsyncIterator

import pytest
from aioinject import Container, InjectionContext
from sqlalchemy.orm import Session

from core.container import create_container
from core.users.schemas import UserCreateSchema, UserSchema
from core.users.services import UserTgService
from core.words.services import WordService

pytest_plugins = ["tests.db_conftest"]


@pytest.fixture(scope="session")
def container() -> Container:
    return create_container()


async def context(container: Container) -> AsyncIterator[InjectionContext]:
    async with container.context() as ctx:
        yield ctx


@pytest.fixture()
async def word_service(context: InjectionContext) -> WordService:
    return await context.resolve(WordService)


@pytest.fixture()
async def user_service(context: InjectionContext) -> UserTgService:
    return await context.resolve(UserTgService)


@pytest.fixture()
async def user(session: Session, user_service: UserTgService) -> UserSchema:
    tg_id = 648253536
    await user_service.create_user(
        UserCreateSchema(
            username="test user",
            email="example@gmail.com",
            tg_id=tg_id,
        ),
        session,
    )
    return await user_service.get_user_by_tg_id(tg_id, session)
