from pydantic import BaseModel, confloat


class Point(BaseModel):
    x: float
    y: float

    def __add__(self, other: 'Point') -> 'Point':
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(x=self.x - other.x, y=self.y - other.y)


class TilePrediction(BaseModel):
    lower_left: Point
    upper_right: Point
    anxiety: confloat(ge=0.0, le=10.0)
