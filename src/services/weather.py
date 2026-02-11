import asyncio
from httpx import AsyncClient
from src.decorators.weather import attempts

from src.utils.base import shutdown_task


class APIClient:
    def __init__(self, http_client: AsyncClient, api_key, retries: int):
        self.http_client = http_client
        self.api_key = api_key
        self.retries = retries

    @attempts(self.retries)
    async def get(self, url):
        async with self.http_client() as client:
            response = await client.get(url=url)
            await response.raise_for_status()
        return response


class WeatherAPI(APIClient):
    def __init__(self, http_client: AsyncClient, api_key: str, retries: int):
        super().__init__(http_client, api_key, retries)

    async def get_current_weather(self, city_name: str):
        return await self.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}")


class WeatherMonitor:
    def __init__(self, timeout: float):
        self.timeout = timeout

    async def run(self, api_get):
        try:
            while True:
                for city in await get_cities_data():
                    await asyncio.sleep(self.timeout)
                    result = await api_get(city.city_name)
                    result and await update_city_weather(result)
        except asyncio.CancelledError:
            pass
        finally:
            print('Weather monitor stop!')


class WeatherManager:
    def __init__(self, http_client: AsyncClient, api_key: str, timeout: float = 24 * 60 * 60 / 500, retries: int = 3):
        self.timeout = timeout
        self.retries = retries
        self.http_client = http_client
        self.api_key = api_key
        self._api_client = None
        self._monitor_task = None

    async def start(self):
        monitor = WeatherMonitor(self.timeout)
        self._api_client = WeatherAPI(http_client=self.http_client, api_key=self.api_key, retries=self.retries)
        self._monitor_task = asyncio.create_task(monitor.run(self._api_client))

    async def stop(self):
        not self._monitor_task.done() and shutdown_task(self._monitor_task)
        self._monitor_task = None
        self._api_client = None

