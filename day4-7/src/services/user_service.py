from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.domain.user import User
from src.models.schemas.user_schema import UserUpdate

class UserService:
    @staticmethod
    async def update_me(db: AsyncSession, current_user: User, user_in: UserUpdate):
        update_data = user_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(current_user, key, value)
        await db.commit()
        await db.refresh(current_user)
        return current_user

    @staticmethod
    async def delete_me(db: AsyncSession, current_user: User):
        await db.delete(current_user)
        await db.commit()
        return {"message": "Tài khoản của bạn đã được xóa vĩnh viễn."}
    @staticmethod
    async def admin_delete_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng này để xóa!")
        
        if user.role == "admin":
            raise HTTPException(status_code=400, detail="Không thể xóa một quản trị viên khác bằng cách này!")

        await db.delete(user)
        await db.commit()
        return {"message": f"Quản trị viên đã xóa người dùng ID: {user_id}"}
    @staticmethod
    async def get_all_users(db: AsyncSession):
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users