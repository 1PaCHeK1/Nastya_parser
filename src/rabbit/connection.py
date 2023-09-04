import contextlib
from collections.abc import AsyncIterator

import aio_pika

from settings import RabbitSettings


@contextlib.asynccontextmanager
async def create_connection(
    settings: RabbitSettings,
) -> AsyncIterator[aio_pika.abc.AbstractConnection]:
    connection = await aio_pika.connect_robust(settings.url)
    async with connection:
        yield connection
