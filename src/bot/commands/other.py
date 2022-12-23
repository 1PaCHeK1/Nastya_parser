from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.core.dispatcher import dp
from bot.core import texts
from bot.utils.auth import identify_user, required_login
from core.users.schemas import UserSchema
from bot.keyboards import inline


@dp.message_handler(Command("start"))
@identify_user
async def welcome_command(
    message: types.Message, 
    user:UserSchema|None
):
    if user is None:
        await message.answer(texts.welcome_text, reply_markup=inline.no_auth_start_keyboard)
    else:
        await message.answer(texts.welcome_text_auth)


@dp.message_handler(Command("help"))
async def help_command(message: types.Message, user:UserSchema):
    await message.answer(texts.info_text)
