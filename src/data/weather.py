from typing import Any
from dataclasses import dataclass


@dataclass
class AddedCity:
    city: Any = None
    status: int = None
    message: str = None

@dataclass
class CityPage:
    page: int = None
    total: int = None
    page_data: Any = None


@dataclass
class CityWeather:
    data: Any = None
    status: int = None

@dataclass
class CityDelete:
    status: int = None
    message: str = None