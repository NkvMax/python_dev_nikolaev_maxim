from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


# Author
class AuthorDTO(BaseModel):
    id: int
    login: str
    email: EmailStr


class AuthorCreateDTO(BaseModel):
    login: str = Field(..., min_length=1)
    email: EmailStr


# Blog
class BlogDTO(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None


class BlogCreateDTO(BaseModel):
    owner_id: int
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


# Post
class PostDTO(BaseModel):
    id: int
    header: str
    text: Optional[str] = None
    author_id: int
    blog_id: int


class PostCreateDTO(BaseModel):
    header: str = Field(..., min_length=1)
    text: Optional[str] = None
    author_id: int
    blog_id: int


# SpaceType and EventType
class SpaceTypeDTO(BaseModel):
    id: int
    name: str


class EventTypeDTO(BaseModel):
    id: int
    name: str


# Log
class LogDTO(BaseModel):
    id: int
    datetime: datetime
    user_id: int
    space_type_id: int
    event_type_id: int


class LogCreateDTO(BaseModel):
    datetime: datetime
    user_id: int
    space_type_id: int
    event_type_id: int
