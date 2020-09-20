# import asyncio
# from typing import List, Tuple, Callable
#
# from sqlalchemy.dialects.postgresql import JSONB
# from pydantic import parse_obj_as
# from gino import Gino
#
# # from .models import ...
#
# db = Gino()

async def get_features():
    return {'temp_3': [19], 'prec_3': [2], 'temp_2': [20], 'prec_2': [0], 'temp_1': [17], 'prec_1': [3], 'articl': [2144], 'perc_rel': [0.310168],
	'perc_zur': [0.018190], 'trips': [5739], 'incoming': [1437], 'inside': [1944]}

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

