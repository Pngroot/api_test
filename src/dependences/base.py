from fastapi import Request, HTTPException, status
from src.core.logger import logger


async def is_authorized(request: Request):
    """
    Dependence для проверки, что пользователь авторизован

    :param request: запрос, содержащий файл куки
    """

    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            redis_cache = request.app.state.redis
            result = await redis_cache.get(session_id)
            if result:
                # Передаем в хэндлеры эндпоинтов при необходимости
                return session_id
        except Exception as e:
            logger.error(f"Error accessing Redis cache: {e}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)