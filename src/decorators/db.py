def insert_to_db(func):
    from fastapi import status
    from sqlalchemy.exc import DatabaseError, IntegrityError
    from src.core.database import async_session

    async def wrapper(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
            async with async_session() as session:
                session.add(data)
                await session.commit()
                await session.refresh(data)
            return status.HTTP_201_CREATED, data
        except IntegrityError:
            return status.HTTP_409_CONFLICT, None
        except DatabaseError as e:
            print(e)
            await session.rollback()
            return status.HTTP_500_INTERNAL_SERVER_ERROR, None
        except Exception as e:
            print(e)
            return status.HTTP_500_INTERNAL_SERVER_ERROR, None
    return wrapper


def get_from_db(func):
    from sqlalchemy.exc import DatabaseError
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
        except DatabaseError:
            session.refresh()
        except Exception:
            pass
    return wrapper