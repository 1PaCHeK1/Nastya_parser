from core.mail.services import MailService
from core.users.schemas import UserRegistrationApiDto
from core.users.services import HashService, UserService

from db.models import User


class RegistrationFromApiUseCase:
    def __init__(
        self,
        user_service: UserService,
        mail_service: MailService,
        hash: HashService,
    ) -> None:
        self._user_service = user_service
        self._mail_service = mail_service
        self._hash = hash

    async def execute(self, dto: UserRegistrationApiDto) -> User | None:
        if self._user_service.email_exists(dto.email):
            return None

        user = self._user_service.registration(dto)
        self._user_service.flush()

        token = self._hash.encode_user(user)
        self._mail_service.send(
            to=user.email,
            content=token,
        )

        print(self._hash.decode_user(token))

        return user

