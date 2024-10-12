import redis.asyncio as redis
from app.config import settings

# Initialize Redis client
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

CACHE_TTL = 60


async def cache_get(key):
    return await redis_client.get(key)

async def cache_set(key, value):
    await redis_client.set(key, value, ex=CACHE_TTL)
