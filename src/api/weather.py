from fastapi import APIRouter, Depends, Response
from src.dependences.base import is_authorized
from src.schemas.weather import *
from src.services.weather import *


# Роутер для работы с API погоды - предполагается, что пользователь валидирован на уровне dependence
weather_router = APIRouter(prefix='/cities', dependencies=[Depends(is_authorized)])


@weather_router.post('/')
async def city_add(body: AddCity, response: Response):
    """
    Эндоинт для добавления города в БД

    :param body: тело POST-запроса
    :param response: сущность результата, которому присваивается значение и статус
    """

    result = await add_city(body)
    response.status_code = result.status
    return ({'city_id': result.city.id, 'city_name': result.city.city_name} if result.city
            else {'message': result.message})


@weather_router.get('/')
async def city_list(page: int=0, per_page: int=10):
    """
    Эндпоинт для вывода списка городов и их текущей погоды с учетом указанной страницы

    :param page: запрашиваемая страница
    :param per_page: максимальное количество объектов на странице
    """

    result = await get_city_list(page, per_page)
    return {'page': result.page, 'total': result.total, 'page_data': (result.page_data if result.page_data
                                                                      else 'Not found')}


@weather_router.get('/{city_id}/')
async def city_weather(city_id: int, response: Response):
    """
    Эндпоинт для вывода текущей погоды в городе с соответствующим city_id

    :param city_id: ID города
    :param response: сущность результата, которому присваивается значение и статус
    """

    result = await get_city_weather(city_id)
    response.status_code = result.status
    if result.data:
        return result.data
    return {'message': 'Not found'}


@weather_router.delete('/{city_id}/delete')
async def city_delete(city_id: int, response: Response):
    """
    Эндпоинт для удаления города с соответствующим city_id

    :param city_id: ID города
    :param response: сущность результата, которому присваивается значение и статус
    """
    result = await delete_city(city_id)
    response.status_code = result.status
    return {'message': result.message}





