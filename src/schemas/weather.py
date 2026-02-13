from typing import Optional
from pydantic import BaseModel


class AddCity(BaseModel):
    """
    Тело POST-запроса на добавление города в систему

    :param city_name: название города (указывается на английском)
    :param country_code: (опционально) код страны в формате ISO 3166
    """

    city_name: str
    country_code: Optional[str] = None