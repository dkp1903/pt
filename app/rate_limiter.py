from fastapi import Request, HTTPException
import redis.asyncio as redis
from app.config import settings

# Initialize Redis client
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

# Maximum requests allowed per minute
RATE_LIMIT = 10

# Rate limiting middleware
async def rate_limiter(func):
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        client_ip = request.client.host

        # Get request count for the client
        request_count = await redis_client.get(client_ip)
        if request_count and int(request_count) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Increment request count
        await redis_client.incr(client_ip)
        await redis_client.expire(client_ip, 60)  # Reset after 1 minute

        # Proceed with original function
        return await func(*args, **kwargs)
    
    return wrapper
