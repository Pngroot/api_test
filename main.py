from fastapi import FastAPI, Depends, Response
from contextlib import asynccontextmanager
from src.core.database import init_db, async_engine
from src.core.cache import create_redis
from src.api.auth import auth_router
from src.dependences.base import is_authorized
from src.services.base import close_session


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    await init_db(async_engine)
    app.state.redis = create_redis()
    await app.state.redis.ping()
    yield
    await async_engine.dispose()
    await app.state.redis.close()


app = FastAPI(lifespan=db_lifespan, debug=True)
app.include_router(auth_router)


@app.get('/')
async def index():
    return {'message': 'Hello World'}


@app.get('/logout')
async def logout(response: Response, session_id: str = Depends(is_authorized)):
    await close_session(session_id)
    response.delete_cookie('session_id')
    return {'message': 'Logged out'}