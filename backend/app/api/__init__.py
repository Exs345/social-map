import logging

from fastapi import FastAPI

# from ..db import db
# from ..config import config

from .router import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    # @app.on_event("startup")
    # async def init_db():
    #     await db.set_bind(config.DB_URL_NOTIFIER, echo=False)
    #     logger = logging.getLogger('gino')
    #     logger.setLevel(logging.WARNING)

    return app
