from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class user_responce(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
