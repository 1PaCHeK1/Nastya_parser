from collections.abc import Sequence
from anyio.streams.memory import MemoryObjectReceiveStream


class ScraperConsumer:
    bunch_size = 5

    def __init__(
        self,
        # database: Database,
    ) -> None:
        # self._database = database
        self._receive_stream: MemoryObjectReceiveStream[str] | None = None

    def registry_receive_stream(
        self,
        receive_stream: MemoryObjectReceiveStream[str],
    ) -> None:
        self._receive_stream = receive_stream

    async def consume(self) -> None:
        if self._receive_stream is None:
            raise ValueError

        async with self._receive_stream:
            bunched = []
            async for item in self._receive_stream:
                bunched.append(item)
                if len(bunched) == self.bunch_size:
                    await self.save_items(bunched)
                    bunched = []
            if bunched:
                await self.save_items(bunched)

    async def save_items(self, bunched: Sequence[str]) -> None:
        print(bunched)
        # with self._database.session_factory.begin() as session:
        #     ...
