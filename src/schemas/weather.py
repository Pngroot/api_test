from typing import Optional
from pydantic import BaseModel


class AddCity(BaseModel):
    city_name: str
    country_code: Optional[str] = None