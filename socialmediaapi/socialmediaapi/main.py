import logging
from contextlib import asynccontextmanager

import fastapi
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.exception_handlers import http_exception_handler

from socialmediaapi.database import database
from socialmediaapi.logging_conf import configure_logging
from socialmediaapi.routers import post, user

logger = logging.getLogger(__name__)


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = fastapi.FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)
app.include_router(post.router)
app.include_router(user.router)


@app.exception_handler(fastapi.HTTPException)
async def http_exception_handle_logging(request, exec):
    logger.error(f"HTTPException: {exec.status_code} {exec.detail}")
    return await http_exception_handler(request, exec)
