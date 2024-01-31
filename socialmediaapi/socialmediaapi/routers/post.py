import fastapi

from socialmediaapi.database import comment_table, database, post_table
from socialmediaapi.models import post

router = fastapi.APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.post("/post", response_model=post.UserPost, status_code=201)
async def create_post(post: post.UserPostIn):
    data = post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[post.UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post("/comment", response_model=post.Comment, status_code=201)
async def create_comment(comment: post.CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise fastapi.HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)

    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[post.Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=post.UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise fastapi.HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
