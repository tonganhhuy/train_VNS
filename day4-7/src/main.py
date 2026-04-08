from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routers import blog, auth, user
from src.config.database import engine, Base
from src.models.domain.post import Post 
from src.models.domain.user import User 
from src.api.middleware import setup_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="My Personal Blog API",
    description="API cho ứng dụng Blog cá nhân",
    version="1.0.0",
    lifespan=lifespan 
)
setup_cors(app)
app.include_router(blog.router, prefix="/api/v1")
app.include_router(auth.router)
app.include_router(user.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với Blog API!"}