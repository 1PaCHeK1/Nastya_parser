import pytest
import os

from sqlalchemy.orm import Session

from settings import Settings, get_settings
from core.containers import Container
from core.users.schemas import UserCreateSchema, UserSchema
from core.users.services import UserTgService
from core.words.services import WordService


pytest_plugins = [
    "tests.db_conftest"
]


@pytest.fixture()
def config() -> Settings:
    env = "test"
    os.environ["ENV"] = env
    db_config = get_settings(environment=env)
    return db_config


@pytest.fixture()
def container(config: Settings) -> Container:
    _container = Container()
    _container.config.from_pydantic(config)
    _container.wire(packages=["tests", "core", "bot", "parsers"])
    return _container


@pytest.fixture()
def word_service(container: Container) -> WordService:
    return container.word_service()


@pytest.fixture()
def user_service(container: Container) -> UserTgService:
    return container.user_service()


@pytest.fixture()
async def user(session: Session, user_service: UserTgService) -> UserSchema:
    tg_id=648253536
    await user_service.create_user(
        UserCreateSchema(
            username="test user",
            email="example@gmail.com",
            tg_id=tg_id,
        ),
        session
    )
    return await user_service.get_user_by_tg_id(tg_id, session)
