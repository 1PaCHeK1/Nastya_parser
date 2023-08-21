import aio_pika
from collections.abc import AsyncIterator
import contextlib


@contextlib.asynccontextmanager
async def create_channel(
    connection: aio_pika.abc.AbstractConnection,
) -> AsyncIterator[aio_pika.abc.AbstractChannel]:
    channel = await connection.channel()
    async with channel:
        yield channel
