from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi import BackgroundTasks
import time

from app.db.session import async_session
from app.models.models import Post, UserPostLink
from app.schemas.post import PostCreate

def new_post(title):
    time.sleep(2)
    print(f"The new post with title '{title}' was created!")

async def create_post(post_create: PostCreate, background_tasks: BackgroundTasks) -> Post:
    async with async_session() as session:
        post=Post(title=post_create.title)
        session.add(post)
        await session.flush()
        for author_id in post_create.authors:
            session.add(UserPostLink(user_id=author_id, post_id=post.id))
        await session.commit()
    background_tasks.add_task(new_post, post_create.title)
    return post_create

async def get_posts():
    async with async_session() as session:
        result = await session.execute(
            select(Post).options(selectinload(Post.authors))
        )
        return result.scalars().all()


async def remove_post(post_id: int):
    async with async_session() as session:
        post=await session.get(Post, post_id)
        if post:
            await session.delete(post)
            await session.commit()
            return post
        return None
