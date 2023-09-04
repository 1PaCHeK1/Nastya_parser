import re
from typing import Annotated

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aioinject import Inject, inject
from sqlalchemy.orm import Session

from bot.core import texts
from bot.keyboards.callback_enum import BaseData, CallbackDataEnum
from bot.states.registration import RegistrationState
from core.users.schemas import UserCreateSchema
from core.users.services import UserTgService

from .commands import start_registration

router = Router(name="registration-router")


@router.message(
    Command("registration", ignore_case=True),
)
async def registration_message(
    message: types.Message,
):
    no_auth_user = await start_registration(message)
    if no_auth_user:
        await message.answer(texts.username_text)
        await RegistrationState.username.set()
    else:
        await message.answer(texts.already_registered_text)


@router.callback_query(BaseData.filter(F.enum == CallbackDataEnum.registration.value))
async def registration_callback(data: types.callback_query.CallbackQuery):
    await start_registration(data.message)

    await data.message.answer(texts.username_text)
    await RegistrationState.username.set()


@router.message(
    Command("cancel", ignore_case=True),
    # RegistrationState.username,
    # RegistrationState.email,
)
async def cancel_registration(message: types.Message, state: FSMContext):
    await message.answer(texts.cancel_text)
    await state.finish()


@router.message(RegistrationState.username)
async def username_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = message.text
    await message.answer(texts.email_text)
    await RegistrationState.email.set()


@router.message(
    lambda message: not re.match(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        str(message.text),
    ),
    RegistrationState.email,
)
@inject
async def invalid_email_registration(
    message: types.Message,
    state: FSMContext,
    user_service: Annotated[UserTgService, Inject],
):
    await message.reply(texts.invalid_registration_email_text)


@router.message(RegistrationState.email)
@inject
async def email_registration(
    message: types.Message,
    state: FSMContext,
    user_service: Annotated[UserTgService, Inject],
    session: Annotated[Session, Inject],
):
    async with state.proxy() as data:
        data["email"] = message.text
        result = data.as_dict()
    await user_service.create_user(
        UserCreateSchema(
            username=result["username"],
            email=result["email"],
            tg_id=message.from_id,
        ),
        session,
    )

    await message.answer(texts.finish_registration_text)
    await state.finish()
