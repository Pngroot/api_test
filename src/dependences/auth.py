from fastapi import Request, HTTPException, status


async def is_authorized(request: Request):
    session_id = request.cookies.get('session_id')
    if session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)