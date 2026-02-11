from fastapi import Request, HTTPException, status


async def is_authorized(request: Request):
    session_id = request.cookies.get('session_id')
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session_id