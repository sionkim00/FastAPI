from contextlib import asynccontextmanager

import fastapi

from socialmediaapi.database import database
from socialmediaapi.routers import post


# Startup and shutdown events
@asynccontextmanager
async def linespan(app: fastapi.FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = fastapi.FastAPI()

app.include_router(post.router)
