import logging
from contextlib import asynccontextmanager

import fastapi

from socialmediaapi.database import database
from socialmediaapi.logging_conf import configure_logging
from socialmediaapi.routers import post

logger = logging.getLogger(__name__)


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    configure_logging()
    logger.info("Starting FastAPI")
    await database.connect()
    yield
    await database.disconnect()


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(post.router)
