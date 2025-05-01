from fastapi import APIRouter

from app.crud.user import create_user, get_users, update_user, remove_user
from app.models.models import User
from app.schemas.user import UserUpdate, UserRead, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserCreate)
async def create(user: UserCreate):
    return await create_user(user)


@router.get("/", response_model=list[UserRead])
async def list_users():
    return await get_users()


@router.patch("/{user_id}", response_model=UserUpdate)
async def patch_user(user_id: int, user_data: UserUpdate):
    return await update_user(user_id, user_data.email)


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int):
    return await remove_user(user_id)
