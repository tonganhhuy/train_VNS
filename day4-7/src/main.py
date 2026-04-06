from fastapi import FastAPI
from src.api.routers import blog
from src.config.database import engine, Base
from src.models.domain.post import Post 
app = FastAPI(
    title="My Personal Blog API",
    description="API cho ứng dụng Blog cá nhân",
    version="1.0.0"
)

app.include_router(blog.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với Blog API!"}