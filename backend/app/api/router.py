from typing import List

from fastapi import APIRouter

from ..models import Point, TilePrediction


router = APIRouter()
# logger = Logger('Main API')


@router.get('/point/{x_coord}/{y_coord}/predict', response_model=List[TilePrediction])
async def get_point_prediction(x_coord: float, y_coord: float):
    request = Point(x=x_coord, y=y_coord)
    tile_size = Point(x=0.0013, y=0.0033)
    return [
        TilePrediction(lower_left=request-tile_size, upper_right=request+tile_size, anxiety=5)
    ]
