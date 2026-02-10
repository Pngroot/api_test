from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import init_db, async_engine
from src.api.auth import auth_router


@asynccontextmanager
async def db_lifespan(app):
    await init_db(async_engine)
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=db_lifespan)
app.include_router(auth_router, prefix="/auth")