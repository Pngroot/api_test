async def shutdown_task(task):
    import asyncio

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass