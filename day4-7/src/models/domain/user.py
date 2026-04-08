from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # BẮT BUỘC: Không bao giờ lưu mật khẩu thường, chỉ lưu mật khẩu đã băm (hashed)
    hashed_password = Column(String(255), nullable=False)
    
    # Phân quyền: Mặc định ai đăng ký cũng là 'user'. Chỉ tạo bằng tay nếu muốn làm 'admin'
    role = Column(String(20), default="user") 
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(255), nullable=True)