from contextlib import AbstractContextManager
from typing import Annotated, Any, Callable
from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aioinject import Inject
from aioinject.ext.fastapi import inject as ai_inject

from sqlalchemy.orm import Session

from core.containers import Container
from core.users.services import UserTgService



class IdentifyUserFilter(Filter):
    @ai_inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        user_service: Annotated[UserTgService, Inject],
        session: Annotated[Session, Inject],
        state: FSMContext = None,
        *args,
        **kwargs,
    ) -> dict[str, Any] | bool:

        user_id = message.from_user.id
        user = await user_service.get_user_by_tg_id(user_id, session)

        return {
            "user": user,
        }


class RequiredUserFilter(Filter):
    @ai_inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        user_service: Annotated[UserTgService, Inject],
        session: Annotated[Session, Inject],
        config: Any,
        state: FSMContext = None,
        *args,
        **kwargs,
    ) -> dict[str, Any] | bool:
        user_id = message.from_user.id
        user = await user_service.get_user_by_tg_id(user_id, session)

        if user is None:
            await message.answer("Сначала нужно авторизоваться!")
            return False

        return {
            "user": user,
        }
