from typing import Annotated
from aiogram import types
from aioinject import inject, Inject

from sqlalchemy.orm import Session

from core.users.services import UserTgService


@inject
async def start_registration(
    message: types.Message,
    user_service: Annotated[UserTgService, Inject],
    session: Annotated[Session, Inject],
) -> bool:
    """Функция начала регистрации"""
    if await user_service.check_user(message.from_user.id, session):
        return False
    return True
