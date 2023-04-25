from contextlib import AbstractContextManager
from typing import Any, Callable
from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from sqlalchemy.orm import Session

from core.containers import Container
from core.users.services import UserService



class IdentifyUserFilter(Filter):
    @inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        state: FSMContext = None,
        user_service: UserService = Provide[Container.user_service],
        get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
        *args,
        **kwargs,
    ) -> dict[str, Any] | bool:

        user_id = message.from_user.id
        with get_session() as session:
            user = await user_service.get_user_by_tg_id(user_id, session)

        return {
            "user": user,
        }


class RequiredUserFilter(Filter):
    @inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        config: Any,
        state: FSMContext = None,
        user_service: UserService = Provide[Container.user_service],
        get_session: Callable[..., AbstractContextManager[Session]] = Provide[Container.database.provided.session],
        *args,
        **kwargs,
    ) -> dict[str, Any] | bool:
        user_id = message.from_user.id
        with get_session() as session:
            user = await user_service.get_user_by_tg_id(user_id, session)

        if user is None:
            await message.answer("Сначала нужно авторизоваться!")
            return False

        return {
            "user": user,
        }
