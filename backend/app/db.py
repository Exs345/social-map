import asyncio
from typing import List, Callable

from sqlalchemy.dialects.postgresql import JSONB
from pydantic import parse_obj_as
from gino import Gino

# from .models import ...

db = Gino()

