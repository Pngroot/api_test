from fastapi import APIRouter, Depends
from src.dependences.base import is_authorized


weather_router = APIRouter('/weather', dependencies=[Depends()])


