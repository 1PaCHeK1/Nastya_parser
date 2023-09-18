from aiogram import Router, types
from aiogram.filters import Command
from aioinject.ext.fastapi import inject

from broker.tasks import reminder_bot_task

router = Router(name="remind")


command_name = "remind"

@router.message(
    Command("remind", ignore_case=True),
    # RequiredUserFilter(),
)
@inject
async def remind_handler(message: types.Message):
    try:
        seconds, message_text = (
            message.text
            .removeprefix(f"/{command_name}")
            .strip()
            .split(maxsplit=1)
        )
        seconds = int(seconds)
    except ValueError:
        await message.answer("Не корректный ввод")
    else:
        await reminder_bot_task.kiq(
            sleep_seconds=int(seconds),
            chat_id=message.chat.id,
            message=message_text,
        )
