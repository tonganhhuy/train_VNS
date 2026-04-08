# My Personal Blog API (FastAPI)

Hệ thống Backend hoàn chỉnh cho ứng dụng Blog cá nhân, hỗ trợ xác thực JWT, phân quyền Role-based, xử lý tác vụ nền (Background Tasks) và được đóng gói toàn bộ bằng Docker.

---

##  Tech Stack
* **Framework:** FastAPI (Python)
* **Cơ sở dữ liệu:** PostgreSQL (v15)
* **ORM:** SQLAlchemy (Async mode)
* **Migration:** Alembic
* **Security:** JWT (JSON Web Token), Bcrypt Hashing
- **DevOps:** Docker & Docker Compose

##  Features (Tính năng chính)
- **Authentication:** Đăng ký & Đăng nhập an toàn. Mật khẩu được Hash (không lưu plain text).
- **Authorization:** Phân quyền người dùng (ADMIN / USER).
- **CRUD Articles:** Quản lý toàn diện bài viết (Viết, Đọc, Sửa, Xóa).
- **Background Tasks:** Tự động gửi Email chào mừng khi đăng ký thành công (chạy ngầm).
- **CORS Middleware:** Cấu hình sẵn sàng kết nối với các ứng dụng Frontend.

---

##  Project Structure (Cấu trúc chi tiết)

Dự án được tổ chức theo mô hình phân lớp (Layered Architecture):

```text
blog-api/
├── src/
│   ├── api/
│   │   ├── routers/             # Tầng định nghĩa API Endpoints
│   │   │   ├── auth.py          # Xử lý Đăng ký, Đăng nhập
│   │   │   ├── blog.py          # Xử lý bài viết (Articles)
│   │   │   └── user.py          # Xử lý thông tin người dùng
│   │   └── middleware.py        # Chốt chặn kiểm tra (CORS)
│   ├── config/                  # Cấu hình hệ thống
│   │   ├── database.py          # Kết nối PostgreSQL (Async)
│   │   └── settings.py          # Quản lý biến môi trường
│   ├── core/                    # Lõi bảo mật
│   │   └── security.py          # Hashing mật khẩu & JWT
│   ├── deps/                    # Dependencies (Phụ thuộc)
│   │   └── auth_deps.py         # Kiểm tra Token & Phân quyền
│   ├── models/                  # Định nghĩa cấu trúc Database (ORM)
│   │   ├── domain/              # SQLAlchemy Models (post.py, user.py)
│   │   └── schemas/             # Pydantic Schemas (Dữ liệu In/Out)
│   ├── services/                # Tầng xử lý Logic nghiệp vụ
│   │   ├── auth_service.py
│   │   ├── blog_service.py
│   │   ├── email_service.py     # Xử lý gửi Mail ngầm
│   │   └── user_service.py
│   └── main.py                  # Entry point - Khởi chạy ứng dụng
├── alembic/                     # Quản lý lịch sử thay đổi Database
│   ├── versions/                # Danh sách các bản Migration chi tiết
│   └── env.py                   # Cấu hình môi trường cho Alembic
├── .env.example                 # File mẫu hướng dẫn cấu hình môi trường
├── .gitignore                   # Loại bỏ file rác và file bảo mật (.env)
├── alembic.ini                  # File cấu hình chính của Alembic
├── docker-compose.yml           # Điều phối Container (Web + DB)
├── Dockerfile                   # Công thức đóng gói ứng dụng
├── requirements.txt             # Danh sách thư viện Python
└── README.md                    # Tài liệu hướng dẫn sử dụng

##  Run With Docker (Hướng dẫn khởi chạy)

Yêu cầu máy tính cài sẵn **Docker Desktop**.

1. **Khởi động hệ thống (Web + DB):**
   ```bash
   docker-compose up -d --build
   ```
2. **Truy cập Swagger Docs (Giao diện test API):**
    [http://localhost:8000/docs](http://localhost:8000/docs)
3. **Dừng hệ thống:**
   ```bash
   docker-compose down
   ```

###  Reset Database (Làm mới dữ liệu)
Xóa sạch dữ liệu cũ và đúc lại toàn bộ bảng:
```bash
docker-compose down -v
docker-compose up -d
```

---

##  Authentication Flow (Luồng xác thực)

1. **Đăng ký:** Gọi `POST /api/v1/auth/register` (Nhận email chào mừng chạy ngầm).
2. **Đăng nhập:** Gọi `POST /api/v1/auth/login` để lấy `access_token`.
3. **Sử dụng:** Gắn token vào Header của các request cần bảo mật:
   `Authorization: Bearer <access_token>`

---

##  Roles and Permissions (Phân quyền)

Hệ thống phân chia quyền hạn chặt chẽ thành 2 cấp độ rõ ràng:

* ** User (Người dùng thông thường):**
  - Được phép đăng bài viết mới.
  - Có toàn quyền (Sửa/Xóa) đối với những bài viết do chính mình tạo ra.
  - Không thể can thiệp vào bài viết của người khác hay quản lý hệ thống.

* ** Admin (Quản trị viên):**
  - Có tất cả các quyền cơ bản của User.
  - Có đặc quyền xem danh sách toàn bộ hệ thống và Xóa tài khoản của người dùng khác.

---

##  Main API Endpoints

###  Articles (Quản lý bài viết)
* `GET /api/v1/articles/`: Lấy danh sách tất cả bài viết.
* `POST /api/v1/articles/`: Tạo một bài viết mới (🔒).
* `GET /api/v1/articles/{post_id}`: Xem chi tiết bài viết.
* `PUT /api/v1/articles/{post_id}`: Cập nhật bài viết (🔒).
* `DELETE /api/v1/articles/{post_id}`: Xóa bài viết (🔒).

###  Authentication
* `POST /api/v1/auth/register`: Đăng ký tài khoản.
* `POST /api/v1/auth/login`: Đăng nhập & lấy Token.

###  Users
* `PUT /api/v1/users/me`: Cập nhật Profile cá nhân (🔒).
* `DELETE /api/v1/users/me`: Xóa tài khoản của chính tôi (🔒).
* `GET /api/v1/users/`: Xem danh sách User (🔒 Chỉ Admin).
* `DELETE /api/v1/users/{user_id}`: Xóa User (🔒 Chỉ Admin).