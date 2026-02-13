from fastapi import Request, HTTPException, status
from src.core.logger import logger


async def is_unauthorized(request: Request):
    session_id = request.cookies.get('session_id')
    if session_id:
        result = None
        try:
            redis_cache = request.app.state.redis
            result = await redis_cache.get(session_id)
        except Exception as e:
            logger.error(f"Error accessing Redis cache: {e}")
        if result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

