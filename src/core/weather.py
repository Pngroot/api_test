from src.core.settings import WEATHER_API_KEY
from src.tasks.weather import WeatherAPIManager
from src.core.logger import logger


async def weather_api_listener():
    if not WEATHER_API_KEY:
        logger.error('WEATHER_API_KEY not set')
        return None
    return WeatherAPIManager(api_key=WEATHER_API_KEY)
