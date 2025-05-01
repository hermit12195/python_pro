from typing import Optional, List

from pydantic import BaseModel

from app.models.models import User


class PostRead(BaseModel):
    id: int
    title: str
    plot: str | None
    authors: List[User]

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    plot: Optional[str] = None
    authors: List[int]