async def close_session(session_id):
    from src.utils.cache import rm_cache

    await rm_cache(session_id)