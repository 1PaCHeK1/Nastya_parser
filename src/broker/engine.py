from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from taskiq import AsyncBroker, InMemoryBroker
from broker.middlewares import InjectMiddleware

from settings import BrokerSettings

settings = BrokerSettings()


broker = InMemoryBroker()


@asynccontextmanager
async def create_broker() -> AsyncIterator[AsyncBroker]:
    broker.middlewares.append(InjectMiddleware)

    await broker.startup()
    yield broker
    await broker.shutdown()
