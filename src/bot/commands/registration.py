import re
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from bot.keyboards.callback_enum import CallbakDataEnum

from core.containers import Container, Provide, inject
from core.users.schemas import UserCreateSchema
from core.users.services import UserService
from bot.core import texts
from bot.core.dispatcher import dp
from bot.states.registration import RegistrationState


@inject
async def start_registration(
    message: types.Message, 
    user_service: UserService = Provide[Container.user_service]
):

    """Функция начала регистрации"""
    if await user_service.check_user(message.from_id):
        return await message.answer(texts.already_registered_text)

    await message.answer(texts.username_text)
    await RegistrationState.username.set()


@dp.message_handler(Command("registration", ignore_case=True))
async def registration_message(
    message: types.Message, 
):
    await start_registration(message)


@dp.callback_query_handler(lambda o: o.data == CallbakDataEnum.registration.value)
async def registration_callback(data: types.callback_query.CallbackQuery):
    await start_registration(data.message)


@dp.message_handler(Command("cancel", ignore_case=True), state=[
    RegistrationState.username,
    RegistrationState.email,
])
async def cancel_registration(message: types.Message, state: FSMContext):
    await message.answer(texts.cancel_text)
    await state.finish()


@dp.message_handler(state=RegistrationState.username)
async def username_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = message.text
    await message.answer(texts.email_text)
    await RegistrationState.email.set()


@dp.message_handler(
    lambda message: not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    message.text),
    state=RegistrationState.email
)
@inject
async def email_registration(
    message: types.Message, 
    state: FSMContext,
    user_service: UserService = Provide[Container.user_service]
):
    await message.reply(texts.invalid_registration_email_text)


@dp.message_handler(state=RegistrationState.email)
@inject
async def email_registration(
    message: types.Message, 
    state: FSMContext,
    user_service: UserService = Provide[Container.user_service],):
    async with state.proxy() as data:
        data["email"] = message.text
        result = data.as_dict()

    await user_service.create_user(
        UserCreateSchema(
            username=result["username"],
            email=result["email"],
            tg_id=message.from_id,
        )
    )

    await message.answer(texts.finish_registration_text)
    await state.finish()
