from main import app, logger


redis = app.state.redis


async def add_to_cache(key, value, ttl=None):
    import json

    try:
        await redis.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        logger.error(f"Error saving data to Redis: {e}")


async def _iter_scan_keys(pattern):
    try:
        async for key in redis.scan_iter(match=pattern):
            yield key
    except TypeError:
        # For older versions
        async for key in redis.scan_iter(pattern):
            yield key


async def rm_cache(pattern, batch_size=500):
    to_delete = []
    async for key in _iter_scan_keys(pattern):
        to_delete.append(key)
        if len(to_delete) >= batch_size:
            await redis.delete(*to_delete)
            to_delete = []
    to_delete and await redis.delete(*to_delete)
