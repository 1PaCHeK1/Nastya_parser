import json
import re
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from core.containers import Container, Provide, inject
from core.users.schemas import UserCreate
from core.users.services import UserService
from core.utils.services import RedisService

from bot.core.dispatcher import dp
from bot.states.registration import RegistrationState


@dp.message_handler(Command("registration", ignore_case=True))
@inject
async def start_registration(
    message: types.Message, 
    user_service: UserService = Provide[Container.user_service]
):
    if await user_service.check_user(message.from_id):
        return await message.answer("Already registrated")

    await message.answer("USERNAME")
    await RegistrationState.username.set()


@dp.message_handler(Command("cancel", ignore_case=True), state=[
    RegistrationState.username,
    RegistrationState.email,
])
async def cancel_registration(message: types.Message, state: FSMContext):
    await message.answer("CANCEL")
    await state.finish()


@dp.message_handler(state=RegistrationState.username)
async def username_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = message.text
    await message.answer("EMAIL")
    await RegistrationState.email.set()



@dp.message_handler(
    lambda message: not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", message.text),
    state=RegistrationState.email
)
@inject
async def email_registration(
    message: types.Message, 
    state: FSMContext,
    user_service: UserService = Provide[Container.user_service]
):
    await message.reply("Invalid email")


@dp.message_handler(state=RegistrationState.email)
@inject
async def email_registration(
    message: types.Message, 
    state: FSMContext,
    user_service: UserService = Provide[Container.user_service],
):
    async with state.proxy() as data:
        data["email"] = message.text
        result = data.as_dict()

    await user_service.create_user(
        UserCreate(
            username=result["username"],
            email=result["email"],
            tg_id=message.from_id,
        )
    )

    await message.answer("FINISH")
    await state.finish()
