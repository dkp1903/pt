from fastapi import Request, HTTPException
import redis.asyncio as redis
from app.config import settings
from functools import wraps

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

RATE_LIMIT = 10

def rate_limiter(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        if not request:
            raise HTTPException(status_code=400, detail="Request object missing")

        client_ip = request.client.host

        request_count = await redis_client.get(client_ip)
        if request_count and int(request_count) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        await redis_client.incr(client_ip)
        await redis_client.expire(client_ip, 60)  # Reset after 1 minute

        return await func(*args, **kwargs)
    
    return wrapper
