from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from src.deps.auth_deps import get_current_user
from src.config.database import engine
from src.models.domain.post import Post
from sqlalchemy.orm import sessionmaker

# KHI DÙNG PREFIX: Toàn bộ các API bên dưới sẽ tự động được gắn thêm "/api/v1/articles" ở phía trước
router = APIRouter(prefix="/articles", tags=["Articles"])

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

class PostCreate(BaseModel):
    title: str
    content: str
    author: str
    topic: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    topic: Optional[str] = None
    is_published: Optional[bool] = None


# --- CÁC HÀM XỬ LÝ (Không cần gõ lại chữ articles nữa) ---

@router.post("/", summary="Create a new article", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        author=post.author,
        topic=post.topic
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return {"message": "Tạo bài viết thành công!", "data": new_post}


@router.get("/", summary="Get all articles")
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return {"message": "Thành công", "total": len(posts), "data": posts}


@router.get("/{post_id}", summary="Get article details")
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết này!")
    return {"message": "Thành công", "data": post}


@router.put("/{post_id}", summary="Update an article")
async def update_post(post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để sửa!")

    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value) 
    await db.commit()
    await db.refresh(post)
    return {"message": "Cập nhật thành công!", "data": post}


@router.delete("/{post_id}", summary="Delete an article")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để xóa!")

    await db.delete(post)
    await db.commit()
    return {"message": f"Đã xóa vĩnh viễn bài viết số {post_id}"}