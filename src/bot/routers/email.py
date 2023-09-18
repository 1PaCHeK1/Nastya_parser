from aiogram import Router, types
from aiogram.filters import Command
from bot.filters.auth import RequiredUserFilter
from core.mail.services import MailService
from core.users.schemas import UserSchema
from core.mail.dto import EmailMessageDto
from typing import Annotated
from aioinject import Inject, inject

router = Router(name="email")


@router.message(
    Command("send_email", ignore_case=True),
    RequiredUserFilter()
)
@inject
async def send_email(
    message: types.Message,
    user: UserSchema,
    email_service: Annotated[MailService, Inject]
) -> None:
    if user.email:
        await email_service.send(EmailMessageDto([user.email], "title", "message"))
        message.answer("Письмо отправлено Вам на почту!")
    else:
        message.answer("Ваша почта не указана")