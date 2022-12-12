from aiogram import types
from aiogram.dispatcher import FSMContext
from functools import wraps
from dependency_injector.wiring import Provide, inject

from core.containers import Container
from core.users.services import UserService

from bot.core import texts


def required_login(f):
    """Обязательно требовать регистрации"""
    
    @wraps(f)
    @inject
    async def wrapper(
        message: types.Message,
        state: FSMContext = None,
        user_service: UserService = Provide[Container.user_service],
    ):
        user = await user_service.get_user_by_tg_id(message.from_id)
        if user is None:
            return await message.answer(texts.not_auth_text)
        if state is None:
            return await f(message, user=user)
        else:
            return await f(message, state, user=user)

    return wrapper


def identify_user(f):
    """Добавляет в параметры объект пользователя если он авторизирован"""

    @wraps(f)
    @inject
    async def wrapper(
        message: types.Message,
        state: FSMContext = None, 
        user_service: UserService = Provide[Container.user_service],
    ):
        user = await user_service.get_user_by_tg_id(message.from_id)
        if state is None:
            return await f(message, user=user)
        else:
            return await f(message, state, user=user)

    return wrapper