from sqlalchemy.orm import Session, joinedload

from db.models import Token


class NoAuthError(Exception):
    ...


def authenticate(
    session: Session,
    token: str,
) -> Token:
    token = session.get(Token, token, options=[joinedload(Token.user)])

    if token is None:
        raise NoAuthError

    return token
