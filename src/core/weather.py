from src.core.settings import WEATHER_API_KEY


async def weather_api_listener():
    if not WEATHER_API_KEY:
        print('WEATHER_API_KEY not set')
        return
