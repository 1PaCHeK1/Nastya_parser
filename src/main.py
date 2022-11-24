from aiogram import executor

from core.containers import Container, Provide, inject
from core.users.services import UserService
from core.utils.services import RedisService

from bot.core.dispatcher import dp


@dp.message_handler(commands=["start"])
async def welcome_command(message):
    print("asdasdasdasd")
    await message.reply("HELLO!")


async def on_startup(dp):
    ...


def main():
    executor.start_polling(
        dp, 
        on_startup=on_startup,
    )


if __name__ == "__main__":
    main()
