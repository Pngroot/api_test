async def hash_password(password):
    from passlib.hash import argon2

    password_hash = argon2.hash(password)
    return password_hash


async def verify_password(password, password_hash):
    from passlib.hash import argon2

    return argon2.verify(password, password_hash)


async def create_user(username, password):
    from fastapi import status
    from sqlalchemy.exc import IntegrityError
    from src.db_requests.auth import create_user
    from src.data.auth import UserRegistered

    user, error = await create_user(username, password)
    if user:
        return UserRegistered(user=user, status=status.HTTP_201_CREATED)
    error_messages = {status.HTTP_409_CONFLICT: 'User already exists!',
                      status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'}
    error_status = (status.HTTP_409_CONFLICT if issubclass(error, IntegrityError)
                    else status.HTTP_500_INTERNAL_SERVER_ERROR)
    return UserRegistered(user=None, status=error_status, message=error_messages[error_status])


async def create_session(user_id):
    import secrets
    from src.utils.cache import add_to_cache

    session_id = secrets.token_urlsafe(32)
    await add_to_cache(session_id, user_id, 60 * 60)
    return session_id


async def authorize(user_data):
    from fastapi import status
    from src.db_requests.auth import get_user_data
    from src.data.auth import UserLogin

    existed_user = await get_user_data(user_data.username)
    if not existed_user:
        return UserLogin(status=status.HTTP_404_NOT_FOUND, session_id=None, message='User not exists!')
    password_match = await verify_password(user_data.password, existed_user['password_hash'])
    if password_match is False:
        return UserLogin(status=status.HTTP_400_BAD_REQUEST, session_id=None, message='Invalid password')
    session_id = await create_session(existed_user['id'])
    return UserLogin(status=status.HTTP_200_OK, session_id=session_id,
                     message=f"You have successfully logged in as {existed_user['username']}")





