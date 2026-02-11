from fastapi import APIRouter, Response, Request, status
from fastapi.responses import RedirectResponse
from src.schemas.auth import *
from src.services.auth import *


auth_router = APIRouter()


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


@auth_router.get('/logout')
async def logout(request: Request):
    session_id = request.cookies.get('session_id')
    if not session_id:
        return RedirectResponse(url='/', status_code=status.HTTP_400_BAD_REQUEST)
    await close_session(session_id)
    response = RedirectResponse(url='/', status_code=status.HTTP_200_OK)
    response.delete_cookie('session_id')
    return response
