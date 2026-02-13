import asyncio
from httpx import AsyncClient
from src.decorators.api import allow_retries
from src.utils.base import shutdown_task
from src.db_requests.weather import get_cities_data, update_city_weather
from src.core.logger import logger


class APIClient:
    """
    TODO: Добавить новые HTTP-запросы в будущем
    """

    def __init__(self, base_url, api_key: str, retries: int):
        self.httpx_client = AsyncClient(base_url=base_url)
        self.api_key = api_key
        self.retries = retries

    @allow_retries
    async def get(self, url):
        """
            Отправляет GET-запрос через HTTPX
        """

        response = await self.httpx_client.get(url=url)
        return response.json()

    async def close(self):
        """
            Закрывает асинхронную HTTPX-сессию
        """

        await self.httpx_client.aclose()
        self.httpx_client = None

    @property
    def closed(self):
        return self.httpx_client.is_closed


class WeatherAPIClient:
    """
    Класс для API запросов к OpenWeatherMap
    """

    base_url = 'https://api.openweathermap.org'

    def __init__(self, api_key: str, retries: int = 1):
        self.api_client = APIClient(self.base_url, api_key, retries)

    async def get_current_weather(self, city_id, city_name):
        """
        GET-запрос к API для получения информации об актуальной погоде в городе
        """

        # Передаем city_name и API-ключ по ссответствующему запросу
        result = await self.api_client.get(f"/data/2.5/weather?q={city_name}&appid={self.api_client.api_key}&lang=ru")
        # При успешном запросе обновляем данные в таблице Weather
        result and await update_city_weather(city_id, result['weather'][0], result['main'])

    async def close_api_client(self):
        """
        Осуществляет закрытие HTTPX-сессии API-клиента
        """

        await self.api_client.close()
        self.api_client = None

    @property
    def api_client_closed(self):
        return self.api_client.closed


class WeatherAPIListener:
    """
    Класс, отвещающий за задачу периодического обращения к API для получения новых данных
    """

    def __init__(self, timeout: float):
        self.timeout = timeout

    async def run(self, api_request):
        """
        Задача по периодическому обращению к API
        """

        logger.info('Weather monitor started!')
        try:
            while True:
                cities = await get_cities_data()
                if cities:
                    # Если есть города в БД - начинаем обращаться к API
                    for city in cities:
                        await api_request(city['id'], city['city_name'])
                    # Важно: выставляем таймаут согласно ограничению по API
                    await asyncio.sleep(self.timeout)
                else:
                    # Ждем следующей итерации, пока не появятся города в БД
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Weather monitor error: {e}")
        finally:
            logger.info('Weather monitor stop!')


class WeatherAPIManager:
    """
    Класс-менеджер для работы со слушателем API-клиента
    """

    def __init__(self, api_key: str, timeout: float = 24 * 60 * 60 / 500, retries: int = 3):
        # Значение по умолчанию (~500 запросов в день) выставлено,
        # чтобы соответствовать ограничению по запросам к API OpenWeatherMap
        self.timeout = timeout
        self.retries = retries
        self.api_key = api_key
        self._client = None
        self._monitor_task = None

    async def start(self):
        monitor = WeatherAPIListener(self.timeout)
        self._client = WeatherAPIClient(api_key=self.api_key, retries=self.retries)
        self._monitor_task = asyncio.create_task(monitor.run(self._client.get_current_weather))
        logger.info('The weather API listener started!')

    async def close(self):
        # Если слушатель не завершен - принудительно закрываем ее
        not self._monitor_task.done() and await shutdown_task(self._monitor_task)
        # Если сессия HTTPX не закрыта - также принудительно закрываем
        not self._client.api_client_closed() and await self._client.close_api_client()
        self._monitor_task = None
        self._client = None
        logger.info('The weather API listener has stopped!')
