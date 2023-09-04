from typing import Annotated, Any, Literal

from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aioinject import Inject, inject
from sqlalchemy.orm import Session

from core.users.services import UserTgService


class IdentifyUserFilter(Filter):
    @inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        user_service: Annotated[UserTgService, Inject],
        session: Annotated[Session, Inject],
        state: FSMContext = None,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        user_id = message.from_user.id
        user = await user_service.get_user_by_tg_id(user_id, session)

        return {
            "user": user,
        }


class RequiredUserFilter(Filter):
    @inject
    async def __call__(
        self,
        message: types.Message | types.CallbackQuery,
        user_service: Annotated[UserTgService, Inject],
        session: Annotated[Session, Inject],
        state: FSMContext = None,
        *args,
        **kwargs,
    ) -> dict[str, Any] | Literal[False]:
        user_id = message.from_user.id
        user = await user_service.get_user_by_tg_id(user_id, session)

        if user is None:
            await message.answer("Сначала нужно авторизоваться!")
            return False

        return {
            "user": user,
        }
