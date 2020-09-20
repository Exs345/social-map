import asyncio
from typing import List

from ..models import Point, TilePrediction
# from ..db import get_features


async def predict_density(x_coord: float, y_coord: float) -> List[TilePrediction]:
    # features = await get_features()
    request = Point(x=x_coord, y=y_coord)
    tile_size = Point(x=0.0013, y=0.0033)
    return [
        TilePrediction.construct_adjusted(request - tile_size, request + tile_size, 75)
    ]
