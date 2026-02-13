async def close_session(session_id):
    """
    Осуществляет выход авторизованного пользователя из системы
    """

    from src.utils.cache import rm_cache

    # Удаляем ID сессии их кэша Redis
    await rm_cache(session_id)