from src.decorators.db import *


@insert_to_db
async def create_user(username, password_hash):
    from src.db.models import User

    user = User(username=username, password_hash=password_hash)
    return user