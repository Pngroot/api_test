from src.decorators.db import *


@insert_to_db
async def create_user(username, password_hash):
    from src.db.models import User

    user = User(username=username, password_hash=password_hash)
    return user


@get_from_db
async def get_user_data(username):
    from sqlalchemy import select
    from src.db.models import User

    q = select(User.id, User.password_hash, User.username).where(User.username == username)
    return q