import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt  # Dùng thẳng thư viện gốc, bỏ qua passlib
from dotenv import load_dotenv

load_dotenv()

# Lấy cấu hình từ file .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def get_password_hash(password: str) -> str:
    """Băm mật khẩu trực tiếp bằng thuật toán chuẩn"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu trực tiếp"""
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Đúc Thẻ từ (JWT)"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt