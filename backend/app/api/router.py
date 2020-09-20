from typing import List

from fastapi import APIRouter

from ..models import TilePrediction
from .inference import predict_density

router = APIRouter()
# logger = Logger('Main API')


@router.get('/point/{x_coord}/{y_coord}/predict', response_model=List[TilePrediction])
async def get_point_prediction(x_coord: float, y_coord: float):
    return await predict_density(x_coord, y_coord)
