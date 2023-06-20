import json
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
from enum import Enum

from settings import RedisSettings
from core.users.schemas import UserSchema


class RedisDbEnum(int, Enum):
    translate_words = 2
    user_words_daily = 3


class RedisService:
    def __init__(self, settings: RedisSettings) -> None:
        self.redis_url = settings.url

    async def get_translations(self, user_id) -> list[str]:
        async with self.get_context(RedisDbEnum.user_words_daily) as redis:
            return json.loads(await redis.get(user_id) or "[]")

    async def get_translate(self, user: UserSchema, word) -> list[str]:
        async with self.get_context(RedisDbEnum.translate_words) as redis:
            translate_words = json.loads(await redis.get(word) or "[]")

        async with self.get_context(RedisDbEnum.user_words_daily) as redis:
            words = json.loads(await redis.get(user.id) or "[]")
            words.append(word)
            await redis.set(user.id, json.dumps(words))

        return translate_words

    async def set_translate(self, word: str, translate_words: list[str]) -> list[str]|None:
        async with self.get_context(RedisDbEnum.translate_words) as redis:
            translate_words_rd = json.loads(await redis.get(word) or "[]")
            translate_words_rd.extend(translate_words)
            await redis.set(word, json.dumps(translate_words_rd))

    @asynccontextmanager
    async def get_context(self, database: RedisDbEnum):
        _redis = aioredis.Redis.from_url(
            self.redis_url,
            db=database.value,
            decode_responses=True
        )

        yield _redis

        await _redis.close()
