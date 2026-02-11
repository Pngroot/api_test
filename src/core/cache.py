import redis.asyncio as aioredis
from src.core.settings import REDIS_URL


if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable not set")


def create_redis():
    return aioredis.from_url(REDIS_URL, encoding='utf-8', decode_responses=True)