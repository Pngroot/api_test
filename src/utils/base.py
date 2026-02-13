async def shutdown_task(task):
    """
        Функция для отмены запущенной задачи
    """

    import asyncio

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass