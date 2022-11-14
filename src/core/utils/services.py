import aioredis


class RedisService:
    def __init__(self, redis_url) -> None:
        self._redis = aioredis.from_url(redis_url, decode_responses=True)

    async def process(self) -> str:
        await self._redis.set("my-key", "value")
        return await self._redis.get("my-key")
