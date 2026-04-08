from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks # 1. BỔ SUNG: Import BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.config.database import get_db
from src.models.domain.user import User
from src.models.schemas.user_schema import UserCreate, UserResponse, Token
from src.core.security import get_password_hash, verify_password, create_access_token
from src.services.email_service import EmailService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where((User.username == user_in.username) | (User.email == user_in.email))
    result = await db.execute(query)
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username hoặc Email đã được sử dụng!")

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    background_tasks.add_task(EmailService.send_welcome_email, new_user.email, new_user.username)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tên đăng nhập hoặc mật khẩu!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}