from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from dotenv import load_dotenv

from src.config.database import get_db
from src.models.domain.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Khai báo vị trí Quầy Lễ Tân để Swagger UI biết đường vẽ cái nút Ổ Khóa
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """Anh bảo vệ 1: Kiểm tra Thẻ JWT xem có hợp lệ không (Dành cho mọi User)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin (Token sai hoặc đã hết hạn)!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Giải mã thẻ JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Soi xuống Database xem user này còn tồn tại không
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Anh bảo vệ 2: Chặn lại nếu không phải là Admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thực hiện hành động này (Yêu cầu quyền Admin)!"
        )
    return current_user