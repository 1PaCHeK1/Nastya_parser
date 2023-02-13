
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import declarative_base, Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_url: str, echo=True) -> None:
        self._engine = create_engine(db_url, echo=echo)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()

    def select_all(self, statement):
        with self.session() as session:
            return session.execute(statement).fetchone().all()


    def select_one(self, statement):
        with self.session() as session:
            return session.execute(statement).one()

    def select_first(self, statement):
        with self.session() as session:
            result = session.execute(statement).scalars()
            if result:
                return result[0]
        return None

    def select_scalar(self, statement):
        with self.session() as session:
            return session.execute(statement).scalar()
