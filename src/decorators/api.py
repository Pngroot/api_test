from src.core.logger import logger


def allow_retries(method):
    """
    Декоратор для организации повторных запросов при обращении к API
    """

    async def wrapper(self, *args, **kwargs):
        retries = self.retries
        attempt = 0
        while True:
            try:
                result = await method(self, *args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error accessing API:\n{e}")
                attempt += 0
                if attempt >= retries:
                    logger.error('The number of API access attempts has been exceeded!')
                    break
    return wrapper