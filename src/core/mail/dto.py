from pydantic import BaseModel


class EmailMessageDto(BaseModel):
    recipients: list[str]
    subject: str
    message: str
