from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.core.dispatcher import dp


dp.message_handler()
async def welcome_command(message: types.Message):
    print("asdasdasdasd")
    await message.reply("HELLO!")
