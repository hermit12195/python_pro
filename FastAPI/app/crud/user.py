from sqlmodel import select

from app.db.session import async_session
from app.models.models import User
from app.schemas.user import UserCreate


async def create_user(user_create: UserCreate) -> User:
    user = User(email=user_create.email)
    async with async_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def update_user(user_id: int, email: str) -> User:
    async with async_session() as session:
        user= await session.get(User, user_id)
        if user:
            user.email = email
            await session.commit()
            await session.refresh(user)
        return user

async def remove_user(user_id: int):
    async with async_session() as session:
        user= await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return user
        else:
            return None