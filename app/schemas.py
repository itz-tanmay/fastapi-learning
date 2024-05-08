from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

# ? Just to make sure this doens't cause undefined error.


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    joined_at: datetime

    class Config:
        from_attributes = True

# ? Posts Schema


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # ? UserResponse will cause error here if UserResponse is defined after.
    owner: UserResponse

    class Config:
        from_attributes = True


class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


# ? User Schemas


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ? Token Schemas

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# ? Votes Schema
class Vote(BaseModel):
    post_id: int
    direction: bool
