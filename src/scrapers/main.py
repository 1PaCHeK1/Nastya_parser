import aiohttp
from anyio import Semaphore, create_task_group, create_memory_object_stream
from anyio.streams.memory import (
    MemoryObjectReceiveStream,
    MemoryObjectSendStream,
)
from .scraper import ScraperProtocol, Concrete1Scraper, Concrete2Scraper
from .consumer import ScraperConsumer


_scrappers: list[type[ScraperProtocol]] = [
    Concrete1Scraper,
    Concrete2Scraper,
    Concrete1Scraper,
    Concrete2Scraper,
    Concrete1Scraper,
    Concrete2Scraper,
]


async def main():
    send_stream: MemoryObjectSendStream[str]
    receive_stream: MemoryObjectReceiveStream[str]
    send_stream, receive_stream = create_memory_object_stream()

    consumer = ScraperConsumer()
    consumer.registry_receive_stream(receive_stream)
    semaphore = Semaphore(initial_value=5)
    async with (
        aiohttp.ClientSession() as client,
        create_task_group() as tg,
    ):
        tg.start_soon(consumer.consume)
        for scraper_cls in _scrappers:
            scraper = scraper_cls(
                client=client,
                send_stream=MemoryObjectSendStream[str](send_stream._state),
                semaphore=semaphore,
            )
            tg.start_soon(scraper.scrape)
        send_stream.close()
