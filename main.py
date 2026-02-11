from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import init_db, async_engine
from src.core.cache import create_redis
from src.api.auth import auth_router


@asynccontextmanager
async def db_lifespan(app):
    await init_db(async_engine)
    app.state.redis = create_redis()
    await app.state.redis.ping()
    yield
    await async_engine.dispose()
    await app.state.redis.close()


app = FastAPI(lifespan=db_lifespan)
app.include_router(auth_router, prefix="/auth")


@app.get('/')
async def index():
    return {'message': 'Hello! You need to log in to continue.'}