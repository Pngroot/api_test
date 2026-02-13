from src.core.logger import logger


def insert_to_db(func):
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
            async with async_session() as session:
                async with session.begin():
                    session.add(data)
                await session.refresh(data)
            return data, None
        except Exception as e:
            logger.error(f"SQLAlchemy INSERT error: {e}")
            error = type(e)
            return None, error
    return wrapper


def get_from_db(func):
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        query = await func(*args, **kwargs)
        try:
            async with async_session() as session:
                query_result = await session.execute(query)
            result = query_result.mappings().one_or_none()
            if result:
                result = dict(result)
            return result
        except Exception as e:
            logger.error(f"SQLAlchemy SELECT (GET) error: {e}")
        return None
    return wrapper


def select_from_db(func):
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        query = await func(*args, **kwargs)
        try:
            async with async_session() as session:
                query_result = await session.execute(query)
                rows = query_result.mappings().all()
            return [dict(r) for r in rows] if rows else []
        except Exception as e:
            logger.error(f"SQLAlchemy SELECT error: {e}")
        return []
    return wrapper


def update_db(func):
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        query = await func(*args, **kwargs)
        try:
            async with async_session() as session:
                query_result = await session.execute(query)
                await session.commit()
            if query_result:
                result = query_result.mappings().one_or_none()
                if result:
                    result = dict(result)
                return result
        except Exception as e:
            logger.error(f"SQLAlchemy UPDATE error: {e}")
        return {}
    return wrapper


def delete_from_db(func):
    from sqlalchemy.exc import NoResultFound
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        query = await func(*args, **kwargs)
        try:
            async with async_session() as session:
                result = await session.execute(query)
                await session.commit()
            if result.rowcount == 0:
                raise NoResultFound
            return True, None
        except Exception as e:
            logger.error(f"SQLAlchemy DELETE error: {e}")
            return False, type(e)
    return wrapper