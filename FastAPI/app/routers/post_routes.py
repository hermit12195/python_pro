from typing import List

from fastapi import APIRouter
from fastapi import BackgroundTasks

from app.crud.post import create_post, get_posts, remove_post
from app.models.models import Post
from app.schemas.post import PostRead, PostCreate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostCreate)
async def create(post: PostCreate, background_tasks: BackgroundTasks):
    return await create_post(post, background_tasks)


@router.get("/", response_model=List[PostRead])
async def get():
    return await get_posts()

@router.delete("/{post_id}", response_model=Post)
async def remove(post_id: int):
    return await remove_post(post_id)