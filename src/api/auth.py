from fastapi import APIRouter, Response, Depends
from src.schemas.auth import *
from src.services.auth import *
from src.dependences.auth import is_unauthorized

# Роутер для работы с авторизацией - предполагается, что пользователь не валидирован на уровне dependence
auth_router = APIRouter(prefix='/auth', dependencies=[Depends(is_unauthorized)])


@auth_router.get('/')
async def auth():
    """
    Эндпоинт-заглушка
    """

    return {'message': 'Login (/auth/login/) or register (/auth/register/)'}


@auth_router.post('/register')
async def register(body: Register, response: Response):
    """
    Эндпоинт для регистрации пользователя в системе

    :param body: тело POST-запроса
    :param response: сущность результата, которому присваивается значение и статус
    """

    hashed_password = await hash_password(body.password)
    result = await create_user(body.username, hashed_password)
    response.status_code = result.status
    return {'id': result.user.id, 'username': result.user.username} if result.user else {'error': result.message}


@auth_router.post('/login')
async def login(body: Register, response: Response):
    """
    Эндпоинт для авторизации пользователя в системе

    :param body: тело POST-запроса
    :param response: сущность результата, которому присваивается значение и статус
    """

    result = await authorize(body)
    response.status_code = result.status
    # При успешной авторизации добавляем session_id в куки пользователя
    result.session_id and response.set_cookie(key='session_id', value=result.session_id, httponly=False)
    return {'message': result.message}
