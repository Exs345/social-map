import asyncio
from typing import List, Tuple, Callable

from sqlalchemy.dialects.postgresql import JSONB
from pydantic import parse_obj_as
from gino import Gino

# from .models import ...

db = Gino()

# async def get_features() -> Tuple[
#     Tuple[temp, prec, desc] (-3, -2, -1),
#     corona cases 1 num,
#     deaths,
#     num of tw posts,
#     num of newspaper ment,
#     % of corona mentionings,
#     1 num long-dist
#     1 num short -dist
# ]

