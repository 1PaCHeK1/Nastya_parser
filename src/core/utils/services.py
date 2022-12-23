import json
import aioredis
from contextlib import asynccontextmanager
from enum import Enum


class RedisDbEnum(int, Enum):
    translate_words = 2
    user_words_daily = 3


class RedisService:
    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url
    
    async def get_translations(self, user_id) -> list[str]:
        async with self.get_context(RedisDbEnum.user_words_daily) as redis:
            return json.loads(await redis.get(user_id) or "[]")
    
    async def get_translate(self, user_id, word) -> str|None:
        async with self.get_context(RedisDbEnum.translate_words) as redis:
            translate_word = await redis.get(word)

        async with self.get_context(RedisDbEnum.user_words_daily) as redis:
            words = json.loads(await redis.get(user_id) or "[]")
            words.append(word)
            await redis.set(user_id, json.dumps(words))

        return translate_word

    @asynccontextmanager
    async def get_context(self, database: RedisDbEnum):
        redis = aioredis.from_url(
            self.redis_url,
            db=database.value,
            decode_responses=True
        )

        yield redis

        await redis.close()
