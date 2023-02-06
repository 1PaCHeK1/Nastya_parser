
import os
import asyncio
import pathlib
import pytest
import sqlalchemy as sa

from typing import Iterable


from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    # async_sessionmaker,
)

from alembic import command, config

from core.config import get_config, Settings
from core.containers import Container


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
    return db_config.database_url


@pytest.fixture(scope="session")
def alembic_config() -> config.Config:
    return config.Config("alembic.ini")


@pytest.fixture(scope="session")
def engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        database_url,
        pool_use_lifo=True,
        pool_size=20,
    )


@pytest.fixture(scope="session")
async def create_database(
    db_config: Settings,
) -> Iterable[None]:
    database_url = f"postgresql+asyncpg://{db_config.db_user}:{db_config.db_password}@{db_config.db_host}:{db_config.db_port}/"  # noqa: E501
    engine = create_async_engine(
        database_url,
        pool_use_lifo=True,
        pool_size=20,
        isolation_level="AUTOCOMMIT",
    )
    async with engine.connect() as conn:
        database_exists = await conn.scalar(
            sa.text(
                f"SELECT datname FROM pg_database WHERE datname='{db_config.db_name}';"
            )
        )
        if not database_exists:
            await conn.execute(
                sa.text(
                    f"CREATE DATABASE {db_config.db_name} OWNER={db_config.db_user};"
                )
            )

    yield

    async with engine.connect() as conn:
        await conn.execute(
            sa.text(
                f"""
                select pg_terminate_backend(pg_stat_activity.pid)
                from pg_stat_activity
                where pg_stat_activity.datname = '{db_config.db_name}'
                and pid <> pg_backend_pid();
                """,
            ),
        )

        await conn.execute(
            sa.text(f"DROP DATABASE IF EXISTS {db_config.db_name} WITH (FORCE);")
        )


@pytest.fixture(scope="session")
async def run_migrations(
    create_database: None,
    engine: AsyncEngine,
    alembic_config: config.Config,
    database_url: str,
) -> None:
    def run_upgrade(connection: Connection, cfg: config.Config) -> None:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, revision="head")

    async with engine.begin() as conn:
        alembic_config.set_main_option("sqlalchemy.url", database_url)
        await conn.run_sync(run_upgrade, alembic_config)
        await conn.commit()


@pytest.fixture()
async def session(
    run_migrations: None,
    engine: AsyncEngine,
) -> AsyncSession:
    async with engine.connect() as conn:
        transaction = await conn.begin()
        sessionmaker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
        )

        async with sessionmaker() as session:
            yield session

        if transaction.is_active:
            await transaction.rollback()
