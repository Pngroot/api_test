from fastapi import APIRouter, Response, Depends
from src.schemas.auth import *
from src.services.auth import *
from src.dependences.auth import is_authorized


auth_router = APIRouter(prefix='/auth', dependencies=[Depends(is_authorized)])


@auth_router.post('/register')
async def register(body: Register, response: Response):
    hashed_password = await hash_password(body.password)
    result = await create_user(body.username, hashed_password)
    response.status_code = result.status
    return {'id': result.user.id, 'username': result.user.username} if result.user else {'error': result.message}


@auth_router.post('/login')
async def login(body: Register, response: Response):
    result = await authorize(body)
    response.status_code = result.status
    result.session_id and response.set_cookie(key='session_id', value=result.session_id, httponly=False)
    return {'message': result.message}
