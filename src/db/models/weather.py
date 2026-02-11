from sqlalchemy import Column, Integer, String, ForeignKey, Float
from src.db.base import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False)
    country_code = Column(String, nullable=True)


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city = ForeignKey('cities.id', ondelete='CASCADE')
    temperature = Column(Float, nullable=True)
    feels_like = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)