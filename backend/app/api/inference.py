import asyncio
import pickle
from typing import List

import pandas as pd
import xgboost as xgb

from ..models import Point, TilePrediction
from ..db import get_features


with open('app/model.pkl', 'rb') as file:
    model = pickle.load(file)


async def predict_density(x_coord: float, y_coord: float) -> List[TilePrediction]:
    data = pd.DataFrame(await get_features())
    # print(X_test)
    score = model.predict(data)[0]
    request = Point(x=x_coord, y=y_coord)
    tile_size = Point(x=0.0006719612516592477, y=0.00064319500257117284)
    return [
        TilePrediction.construct_adjusted(request - tile_size, request + tile_size, score)
    ]
