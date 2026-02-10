from src.decorators.db import *


async def hash_password(password: str):
    import hashlib, os

    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1024)
    return f"{salt}{dk.hex()}"

@insert_to_db
async def create_user(username, password):
    from src.db_requests.auth import create_user

    return await create_user(username, password)




