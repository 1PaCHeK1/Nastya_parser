import aio_pika

from core.mail.dto import EmailMessageDto


class MailService:
    def __init__(
        self,
        channel: aio_pika.abc.AbstractChannel,
    ) -> None:
        self._channel = channel

    async def send(self, message: EmailMessageDto) -> None:
        json_message = message.model_dump_json()
        await self._channel.default_exchange.publish(
            aio_pika.Message(json_message.encode()),
            routing_key="test_queue",
        )
