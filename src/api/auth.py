from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from core.auth import NoAuthError, authenticate as core_authenticate
from db.models import Token


class _BearerToken(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        api_key = await super().__call__(request)
        if not api_key:
            return None
        return api_key.removeprefix("Bearer ")


_auth_scheme = _BearerToken(name="Authorization", auto_error=False)

_unauthorized_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

AuthToken = Annotated[str | None, Depends(_auth_scheme)]


@inject
async def authenticate(
    session: Annotated[Session, Inject],
    token: AuthToken,
) -> Token:
    if token is None:
        raise _unauthorized_exc

    try:
        token = core_authenticate(session, token)
    except NoAuthError:
        raise _unauthorized_exc

    return token


Authenticate = Annotated[Token, Depends(authenticate)]
