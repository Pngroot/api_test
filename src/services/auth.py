async def hash_password(password):
    """
    Простой генератор хэша пароля
    """

    from passlib.hash import argon2

    password_hash = argon2.hash(password)
    return password_hash


async def verify_password(password, password_hash):
    """
    Проверка введенного пользователем пароля с хэшем пароля в БД
    """

    from passlib.hash import argon2

    return argon2.verify(password, password_hash)


async def create_user(username, password):
    """
    Создание пользователя в БД

    :return UserRegistered: dataclass, содержащий информацию о зарегистрированном пользователе, статус-код
    и передаваемое тело сообщения
    """

    from fastapi import status
    from sqlalchemy.exc import IntegrityError
    from src.db_requests.auth import create_user
    from src.data.auth import UserRegistered

    user, error = await create_user(username, password)
    if user:
        return UserRegistered(user=user, status=status.HTTP_201_CREATED)
    error_messages = {status.HTTP_409_CONFLICT: 'User already exists!',
                      status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'}
    # IntegrityError - запись в БД уже существует
    error_status = (status.HTTP_409_CONFLICT if issubclass(error, IntegrityError)
                    else status.HTTP_500_INTERNAL_SERVER_ERROR)
    return UserRegistered(user=None, status=error_status, message=error_messages[error_status])


async def create_session(user_id):
    """
    Генератор ID сессии для авторизованного пользователя.
    """

    import secrets
    from src.utils.cache import add_to_cache

    session_id = secrets.token_urlsafe(32)
    # Сохраняем ID сессии в кэш Redis для ускорения дальнейшей валидации пользователя
    await add_to_cache(session_id, user_id, 60 * 60)
    return session_id


async def authorize(user_data):
    """
    Авторизация пользователя в системе

    :return UserLogin: dataclass, содержащий ID сессии, статус-код и передаваемое тело сообщения
    """

    from fastapi import status
    from src.db_requests.auth import get_user_data
    from src.data.auth import UserLogin

    # Проверяем наличие пользователя в БД
    # TODO: кэшировать запрос
    existed_user = await get_user_data(user_data.username)
    if not existed_user:
        return UserLogin(status=status.HTTP_404_NOT_FOUND, session_id=None, message='User not exists!')
    password_match = await verify_password(user_data.password, existed_user['password_hash'])
    if password_match is False:
        return UserLogin(status=status.HTTP_400_BAD_REQUEST, session_id=None, message='Invalid password')
    # Получаем ID сессии
    session_id = await create_session(existed_user['id'])
    return UserLogin(status=status.HTTP_200_OK, session_id=session_id,
                     message=f"You have successfully logged in as {existed_user['username']}")





