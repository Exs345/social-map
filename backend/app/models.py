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
    score: confloat(ge=30, le=100)

    @classmethod
    def construct_adjusted(cls, lower_left: Point, upper_right: Point, score: float) \
            -> 'TilePrediction':
        score = min(max(score, 30), 100)
        return cls(lower_left=lower_left, upper_right=upper_right, score=score)
