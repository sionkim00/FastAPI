import fastapi

from routers import post

app = fastapi.FastAPI()

app.include_router(post.router)
