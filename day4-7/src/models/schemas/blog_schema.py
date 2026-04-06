from pydantic import BaseModel, Field
from typing import Optional

class BlogBase(BaseModel):
    title: str = Field(..., title="Tiêu đề bài viết", max_length=100)
    content: str = Field(..., title="Nội dung bài viết", min_length=10)
    is_published: bool = False

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int

    class Config:
        from_attributes = True 