import redis.asyncio as redis
from app.config import settings

# Initialize Redis client
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

# Cache TTL (time-to-live) in seconds
CACHE_TTL = 60

# Function to retrieve cached data
async def cache_get(key):
    return await redis_client.get(key)

# Function to cache data with TTL
async def cache_set(key, value):
    await redis_client.set(key, value, ex=CACHE_TTL)
