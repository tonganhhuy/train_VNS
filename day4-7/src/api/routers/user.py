from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Thêm dòng này để hệ thống nhận diện được 'User'
from src.models.domain.user import User 

from src.deps.auth_deps import get_current_user, get_current_admin_user
from src.services.user_service import UserService
from src.models.schemas.user_schema import UserResponse, UserUpdate
from src.config.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# --- NHÓM CÁ NHÂN ---
@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_in: UserUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await UserService.update_me(db, current_user, user_in)

@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_my_account(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await UserService.delete_me(db, current_user)

# --- NHÓM QUẢN TRỊ ---
@router.get("/", response_model=list[UserResponse])
async def read_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return await UserService.get_all_users(db)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_remove_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db), 
    admin: User = Depends(get_current_admin_user) # Chỉ Admin mới vào được đây
):
    return await UserService.admin_delete_user(db, user_id)