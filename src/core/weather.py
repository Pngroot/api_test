from src.core.settings import WEATHER_API_KEY
from src.tasks.weather import WeatherAPIListener


async def weather_api_listener():
    if not WEATHER_API_KEY:
        print('WEATHER_API_KEY not set')
        return None
    return WeatherAPIListener(api_key=WEATHER_API_KEY)
