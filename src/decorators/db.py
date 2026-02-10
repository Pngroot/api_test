def insert_to_db(func):
    from sqlalchemy.exc import IntegrityError, DatabaseError
    from src.core.database import async_session
    from src.data.db import InsertResult

    async def wrapper(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
            async with async_session() as session:
                session.add(data)
                await session.commit()
            return InsertResult(success=True, existed=False, faulted=False)
        except IntegrityError:
            return InsertResult(success=False, existed=True, faulted=False)
        except DatabaseError:
            await async_session.rollback()
            return InsertResult(success=False, existed=False, faulted=True)
        except Exception:
            return InsertResult(success=False, existed=False, faulted=True)
    return wrapper