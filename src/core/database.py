from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.settings import DB_URL, ALEMBIC_DB_URL
from src.db.base import Base


if not DB_URL:
    raise ValueError("DB_URL environment variable not set")

if not ALEMBIC_DB_URL:
    raise ValueError("ALEMBIC_DB_URL environment variable not set")

async_engine = create_async_engine(DB_URL)

async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"Loaded tables - {Base.metadata.tables.keys()}")

