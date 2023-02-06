import os
from core.config import Settings, get_config
from core.containers import Container
from core.users.schemas import UserCreateSchema, UserSchema
from core.users.services import UserService
from core.words.services import WordService
import pytest


# plugins_pytest = [ "db_conftest" ]


@pytest.fixture()
def config() -> Settings:
    env = "test"
    os.environ["ENV"] = env
    db_config = get_config(environment=env)
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
def user_service(container: Container) -> UserService:
    return container.user_service()


@pytest.fixture()
async def user(user_service: UserService) -> UserSchema:
    tg_id=648253536
    await user_service.create_user(
        UserCreateSchema(
            username="test user",
            email="example@gmail.com",
            tg_id=tg_id,
        )
    )
    return await user_service.get_user_by_tg_id(tg_id)
