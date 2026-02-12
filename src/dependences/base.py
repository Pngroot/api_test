from fastapi import Request, HTTPException, status


async def is_authorized(request: Request):
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            redis_cache = request.app.state.redis
            result = await redis_cache.get(session_id)
            if result:
                print(f"Session id - {session_id} associate with user id {result}")
                return session_id
        except Exception as e:
            print(e)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)