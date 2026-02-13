async def add_city(data):
    """
    Создание записи о городе в БД

    :return UserRegistered: dataclass, содержащий информацию о добавлеенном городе, статус-код
    и передаваемое тело сообщения
    """

    from fastapi import status
    from sqlalchemy.exc import IntegrityError
    from src.data.weather import AddedCity
    from src.db_requests.weather import add_city_data

    result, error = await add_city_data(data)
    if result:
        return AddedCity(city=result, status=status.HTTP_201_CREATED)
    error_messages = {status.HTTP_409_CONFLICT: 'City already exists!',
                      status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'}
    # IntegrityError - запись в БД уже существует
    error_status = (status.HTTP_409_CONFLICT if issubclass(error, IntegrityError)
                    else status.HTTP_500_INTERNAL_SERVER_ERROR)
    return AddedCity(city=None, status=error_status, message=error_messages[error_status])


async def get_city_list(page, per_page):
    """
    Получение списка городов и их актуальной погоды

    :return CityPage: dataclass, содержащий страницу со списком городов, выбранную страницу
    и максимальное число страниц
    """


    import math
    from src.data.weather import CityPage
    from src.db_requests.weather import get_city_page

    offset = page * per_page
    result = await get_city_page(offset, per_page)
    total = page
    if result:
        # Получаем total и удаляем дублируемое значение из списка городов
        total = math.ceil(result[0]['total'] / per_page)
        result = [{key: value for key, value in city.items() if key != 'total'} for city in result]
    return CityPage(page=page, total=total, page_data=result)


async def get_city_weather(city_id):
    """
    Получение информации о погоде в городе

    :param city_id: ID города
    :return CityWeather: dataclass, содержащий информацию о погоде и статус-код
    """

    from fastapi import status
    from src.data.weather import CityWeather
    from src.db_requests.weather import get_city_data

    result = await get_city_data(city_id)
    if result:
        return CityWeather(data=result, status=status.HTTP_200_OK)
    return CityWeather(data=None, status=status.HTTP_404_NOT_FOUND)


async def delete_city(city_id):
    """
    Удаление города из БД

    :param city_id: ID города
    :return CityDelete: dataclass, содержащий статус-код и тело сообщения
    """

    from fastapi import status
    from sqlalchemy.exc import NoResultFound
    from src.data.weather import CityDelete
    from src.db_requests.weather import delete_city_data

    deleted, error = await delete_city_data(city_id)
    if deleted:
        return CityDelete(status=status.HTTP_200_OK,
                          message=f"City with id = {city_id} was deleted successfully!")
    # NoResultFound - записи в БД не существует
    error_status = (status.HTTP_404_NOT_FOUND if issubclass(error, NoResultFound)
                    else status.HTTP_500_INTERNAL_SERVER_ERROR)
    error_messages = {status.HTTP_404_NOT_FOUND: f"City with id = {city_id} not found!",
                      status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error!'}
    return CityDelete(status=error_status, message=error_messages[error_status])

