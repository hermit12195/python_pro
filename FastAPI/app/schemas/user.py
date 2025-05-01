from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str


class UserRead(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: str