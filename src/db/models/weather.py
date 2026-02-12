from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.db.base import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False, unique=True)
    country_code = Column(String, nullable=True)

    weather = relationship('Weather', back_populates='city', cascade='all, delete-orphan')

class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'))
    weather = Column(String, nullable=True)
    description = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    feels_like = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    city = relationship('City', back_populates='weather')