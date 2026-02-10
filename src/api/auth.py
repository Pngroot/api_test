from fastapi import APIRouter, Response
from src.schemas.auth import *
from src.services.auth import *


auth_router = APIRouter()


@auth_router.post("/register")
async def register(body: Register):
    hashed_password = await hash_password(body.password)
    user = await create_user(body.username, hashed_password)
    if user.success:
        return {'status': 201, 'username': body.username}
    elif user.existed:
        return {'status': 409, 'message': 'User already exists'}
    return {'status': 500, 'message': 'Internal Server Error'}


