from src.decorators.db import *


@insert_to_db
async def add_city_data(city):
    from src.db.models.weather import City, Weather

    city = City(city_name=city.city_name, country_code=city.country_code)
    weather = Weather(weather=None, description=None, temperature=0, feels_like=0,
                      pressure=0, humidity=0, temp_min=0, temp_max=0)
    city.weather.append(weather)
    return city


@select_from_db
async def get_cities_data():
    from sqlalchemy import select
    from src.db.models.weather import City

    q = select(City.id, City.city_name)
    return q


@update_db
async def update_city_weather(city_id, weather, meters):
    from sqlalchemy import update
    from src.db.models.weather import Weather

    q = (update(Weather).where(Weather.city_id == city_id)
         .values(weather=weather['main'],
                 description=weather['description'],
                 temperature=meters['temp'],
                 feels_like=meters['feels_like'],
                 pressure=meters['pressure'],
                 humidity=meters['humidity'],
                 temp_min=meters['temp_min'],
                 temp_max=meters['temp_max'])
         .returning(Weather.weather, Weather.description, Weather.temperature, Weather.feels_like, Weather.pressure,
                    Weather.humidity, Weather.temp_min, Weather.temp_max))
    return q


@select_from_db
async def get_city_page(offset, per_page):
    from sqlalchemy import select, func
    from src.db.models.weather import City, Weather

    q = (select(City.id, City.city_name, Weather.weather, Weather.description, Weather.temperature, Weather.feels_like,
                Weather.temp_min, Weather.temp_max, Weather.pressure, Weather.humidity,
                func.count().over().label("total"))
         .join(Weather, Weather.city_id == City.id)
         .limit(per_page).offset(offset).order_by(City.id))
    return q


@get_from_db
async def get_city_data(city_id):
    from sqlalchemy import select
    from src.db.models.weather import City, Weather

    q = (select(City.id, City.city_name, Weather.weather, Weather.description, Weather.temperature, Weather.feels_like,
                Weather.temp_min, Weather.temp_max, Weather.pressure, Weather.humidity)
         .join(Weather, Weather.city_id == City.id)
         .where(City.id == city_id))
    return q


@delete_from_db
async def delete_city_data(city_id):
    from sqlalchemy import delete
    from src.db.models.weather import City

    q = delete(City).where(City.id == city_id)
    return q