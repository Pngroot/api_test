from fastapi import Request, HTTPException, status


async def is_unauthorized(request: Request):
    session_id = request.cookies.get('session_id')
    if session_id:
        result = None
        try:
            redis_cache = request.app.state.redis
            result = await redis_cache.get(session_id)
        except Exception as e:
            print(e)
        if result:
            print(f"Session id - {session_id} associate with user id {result}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

