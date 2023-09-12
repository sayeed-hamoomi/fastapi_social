from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class user_responce(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    # owner_id: int
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: user_responce

    class config:
        orm_mode = True


class PostWithVotes(BaseModel):
    Post: Post
    votes: int

    class config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
