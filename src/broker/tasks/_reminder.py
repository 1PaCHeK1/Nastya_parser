import asyncio
from typing import Annotated
from aiogram import Bot
from aiogram.methods import SendMessage
from aioinject import inject, Inject
from broker.engine import broker


@broker.task
@inject
async def reminder_bot_task(
    sleep_seconds: int,
    chat_id: int,
    message: str,
    bot: Annotated[Bot, Inject],
) -> None:
    await asyncio.sleep(sleep_seconds)
    send_message = SendMessage(
        chat_id=chat_id,
        text=message,
    )
    await bot(send_message)
