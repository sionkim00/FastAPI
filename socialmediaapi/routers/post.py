import fastapi

from models import post

router = fastapi.APIRouter()


post_table = {}


@router.post("/", response_model=post.UserPost)
async def create_post(post: post.UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post

    return new_post


@router.get("/", response_model=list[post.UserPost])
async def get_all_posts():
    return list(post_table.values())
