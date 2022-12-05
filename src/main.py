from aiogram import executor, Dispatcher, types

from core.containers import Container, Provide, inject
from core.users.services import UserService
from core.utils.services import RedisService

from bot.commands import dp


async def on_startup(dp:Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запуск бота"),
        types.BotCommand("help", "Информация"),
        types.BotCommand("favorites", "Избранные"),
        types.BotCommand("settings", "Настройки"),
        types.BotCommand("list", "Случайные слова"),
    ])
    
    container = Container()
    container.init_resources()
    container.wire(packages=[
        "bot.commands",
    ])


def main():
    executor.start_polling(
        dp, 
        on_startup=on_startup,
    )


if __name__ == "__main__":
    main()
