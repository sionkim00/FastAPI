import fastapi

from socialmediaapi.routers import post

app = fastapi.FastAPI()

app.include_router(post.router)
