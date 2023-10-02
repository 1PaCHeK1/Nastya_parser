import anyio
from aiohttp import ClientSession
from typing import Protocol
from anyio.streams.memory import MemoryObjectSendStream


class ScraperProtocol(Protocol):
    base_url: str

    def __init__(
        self,
        client: ClientSession,
        send_stream: MemoryObjectSendStream[str],
        semaphore: anyio.Semaphore,
        query_params: dict[str, int | str] | None = None,
    ) -> None:
        ...

    async def scrape(self) -> list[str]:
        ...


class Concrete1Scraper(ScraperProtocol):
    base_url = ""

    def __init__(
        self,
        client: ClientSession,
        send_stream: MemoryObjectSendStream[str],
        semaphore: anyio.Semaphore,
        query_params: dict[str, int | str] | None = None,
    ) -> None:
        self._client = client
        self._send_stream = send_stream
        self._query_params = query_params
        self._semaphore = semaphore

    async def scrape(self) -> list[str]:
        async with self._semaphore:
            async with self._send_stream:
                await self._send_stream.send("parser 1")
            await anyio.sleep(5)
        return
        async with self._client.get(
            self.base_url,
            params=self._query_params,
        ) as response:
            await response.json()


class Concrete2Scraper(ScraperProtocol):
    base_url = ""

    def __init__(
        self,
        client: ClientSession,
        send_stream: MemoryObjectSendStream[str],
        semaphore: anyio.Semaphore,
        query_params: dict[str, int | str] | None = None,
    ) -> None:
        self._client = client
        self._send_stream = send_stream
        self._semaphore = semaphore
        self._query_params = query_params

    async def scrape(self) -> None:
        async with self._semaphore:
            async with self._send_stream:
                await self._send_stream.send("parser 2")
            await anyio.sleep(5)
        return
        async with self._client.get(
            self.base_url,
            params=self._query_params,
        ) as response:
            await response.json()
