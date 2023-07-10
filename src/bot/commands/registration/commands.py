from contextlib import AbstractContextManager
from typing import Callable
from aiogram import types
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from core.containers import Container
from core.users.services import UserTgService
from bot.core import texts


@inject
async def start_registration(
    message: types.Message,
    user_service: UserTgService = Provide[Container.user_service],
    get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session]
) -> bool:

    """Функция начала регистрации"""
    with get_session() as session:
        if await user_service.check_user(message.from_user.id, session):
            return False
        return True
