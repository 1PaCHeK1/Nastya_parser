from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.core.dispatcher import dp
from bot.core import texts

@dp.message_handler(Command("start"))
async def welcome_command(message: types.Message):
    await message.answer(texts.welcome_text)


@dp.message_handler(Command("help"))
async def help_command(message: types.Message):
    await message.answer(texts.info_text)
