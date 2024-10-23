from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------------------------- 사용자 스키마 ----------------------------
class UserBase(BaseModel):
    username: str
    email: str
    country: str

class UserCreate(UserBase):
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    country: str
    created_at: datetime

    class Config:
        orm_mode = True

# ---------------------------- 게시글 스키마 ----------------------------
class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    author: User

    class Config:
        orm_mode = True