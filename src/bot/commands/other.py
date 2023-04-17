from aiogram import types, Router
from aiogram.filters import Command
from bot.core import texts
from bot.utils.auth import IdentifyUserFilter
from core.users.schemas import UserSchema
from bot.keyboards import inline


router = Router()


@router.message(
    Command("start"),
    IdentifyUserFilter(),
)
async def welcome_command(
    message: types.Message,
    user: UserSchema | None
):
    if user is None:
        await message.answer(texts.welcome_text, reply_markup=inline.no_auth_start_keyboard)
    else:
        await message.answer(texts.welcome_text_auth)


@router.message(Command("help"))
async def help_command(message: types.Message, user:UserSchema):
    await message.answer(texts.info_text)
