from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session, declarative_base

from settings import DatabaseSettings

Base = declarative_base()


class Database:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._engine = create_engine(
            settings.url,
            echo=settings.echo,
        )
        self.session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )


@contextmanager
def get_session(database: Database) -> Generator[Session]:
    with database.session_factory.begin() as session:
        yield session
