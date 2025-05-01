from typing import Optional, List


from sqlmodel import SQLModel, Field, Relationship

class UserPostLink(SQLModel, table= True):
    user_id: int= Field(foreign_key="user.id", primary_key=True)
    post_id: int = Field(foreign_key="post.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True)
    email: str
    posts: List["Post"] = Relationship(back_populates="authors", link_model=UserPostLink)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True)
    title: str
    plot: Optional[str] = None
    authors: List["User"] = Relationship(back_populates="posts", link_model=UserPostLink)

