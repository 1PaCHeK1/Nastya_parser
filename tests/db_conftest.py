import asyncio
import os
import pathlib
from collections.abc import Iterable

import pytest
import sqlalchemy_utils
from alembic import command, config
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session, sessionmaker

from db.models import Language

base_dir = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def database_url() -> str:
    return os.environ["TEST_DATABASE_URL"]


@pytest.fixture(scope="session")
def alembic_config() -> config.Config:
    return config.Config("alembic.ini")


@pytest.fixture(scope="session")
def engine(database_url: str) -> Engine:
    return create_engine(database_url)


@pytest.fixture(scope="session")
async def create_database(
    database_url: str,
) -> Iterable[None]:
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
        ],
    )
    raw_session.flush()


@pytest.fixture()
def session(raw_session: Session, load_database: None) -> Session:
    yield raw_session
