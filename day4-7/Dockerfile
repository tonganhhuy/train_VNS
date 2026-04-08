# 1. Chọn hệ điều hành có sẵn Python 3.9
FROM python:3.9-slim

# 2. Đặt thư mục làm việc bên trong Container là /app
WORKDIR /app

# 3. Copy file requirements.txt vào trước
COPY requirements.txt .

# 4. Cài công cụ uv trước, sau đó dùng uv cài thư viện siêu tốc
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt

# 5. Copy toàn bộ code (thư mục src) của bạn vào trong Container
COPY . .

# 6. Mở cổng 8000 để giao tiếp ra ngoài
EXPOSE 8000

# 7. Lệnh để chạy ứng dụng khi Container khởi động
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]