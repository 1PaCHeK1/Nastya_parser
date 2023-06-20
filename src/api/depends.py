import functools
from typing import Any, ClassVar, Generic, Iterator, TypeVar
from fastapi import Depends, Request, params
from sqlalchemy.orm import Session
from dependency_injector.wiring import Provide, inject
from core.containers import Container


@inject
def get_session(
    get_session_db = Depends(Provide[Container.database.provided.session]),
) -> Iterator[Session]:
    with get_session_db() as session:
        yield session
