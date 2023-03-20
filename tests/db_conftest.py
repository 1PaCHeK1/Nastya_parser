
import os
import asyncio
import pathlib
import pytest

import sqlalchemy_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Iterable


from sqlalchemy.engine import Connection, Engine

from alembic import command, config

from core.config import get_config, Settings
from core.containers import Container

from core.words.models import Language


base_dir = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_config() -> Settings:
    env = "test"
    os.environ["ENV"] = env
    db_config = get_config(environment=env)
    return db_config


@pytest.fixture(scope="session")
def db_container(db_config: Settings) -> Container:
    _container = Container()
    _container.config.from_pydantic(db_config)
    _container.wire(packages=["tests", "core", "bot", "parsers"])
    return _container


@pytest.fixture(scope="session")
def database_url(db_config: Settings) -> str:
    return db_config.db_url


@pytest.fixture(scope="session")
def alembic_config() -> config.Config:
    return config.Config("alembic.ini")


@pytest.fixture(scope="session")
def engine(database_url: str) -> Engine:
    return create_engine(database_url)


@pytest.fixture(scope="session")
async def create_database(
    db_config: Settings,
) -> Iterable[None]:
    database_url = f"postgresql://{db_config.db_user}:{db_config.db_pass}@{db_config.db_host}:{db_config.db_port}/{db_config.db_name}"  # noqa: E501

    if not sqlalchemy_utils.database_exists(database_url):
        sqlalchemy_utils.create_database(database_url)

    yield

    sqlalchemy_utils.drop_database(database_url)


@pytest.fixture(scope="session")
def run_migrations(
    create_database: None,
    engine: Engine,
    alembic_config: config.Config,
    database_url: str,
) -> None:
    def run_upgrade(connection: Connection, cfg: config.Config) -> None:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, revision="head")

    with engine.begin() as conn:
        alembic_config.set_main_option("sqlalchemy.url", database_url)
        conn.run_callable(run_upgrade, alembic_config)


@pytest.fixture(scope="session")
def raw_session(
    run_migrations: None,
    engine: Engine,
) -> Session:
    with engine.connect() as conn:
        transaction = conn.begin()
        _sessionmaker = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
        )

        with _sessionmaker() as session:
            yield session

        if transaction.is_active:
            transaction.rollback()


@pytest.fixture(scope="session")
def load_database(
    raw_session: Session,
) -> None:
    raw_session.add_all(
        [
            Language(name="ru", order=1),
            Language(name="en", order=2),
        ]
    )
    raw_session.flush()


@pytest.fixture()
def session(
    raw_session: Session,
    load_database: None
) -> Session:
    yield raw_session
