# E-commerce Microservices System

Hệ thống E-commerce dựa trên kiến trúc Microservices, được xây dựng bằng Python (Django REST Framework), MySQL, Docker và Celery.

## 🚀 Tổng quan hệ thống
Hệ thống bao gồm 3 dịch vụ chính hoạt động độc lập:
*   **Auth Service (8001)**: Quản lý người dùng, đăng ký, đăng nhập và xác thực JWT.
*   **Inventory Service (8002)**: Quản lý danh mục sản phẩm, thông tin hàng hóa và tồn kho.
*   **Order Service (8003)**: Quản lý giỏ hàng, đơn hàng và tích hợp gửi email thông báo qua Celery.

### Công nghệ sử dụng
*   **Backend**: Django, Django REST Framework, Djoser (Auth).
*   **Database**: MySQL 8.0.
*   **Containerization**: Docker, Docker Compose.
*   **Background Jobs**: Celery, Redis.

---

## 🛠️ Hướng dẫn cài đặt và khởi chạy

1. **Clone project và tạo file .env**:
   Sao chép file `.env.example` thành `.env` và cấu hình các thông số cần thiết.

2. **Khởi chạy bằng Docker Compose**:
   ```bash
   docker-compose up -d --build
   ```
   Lệnh này sẽ tự động:
   *   Xây dựng các Docker images cho từng service.
   *   Khởi chạy database MySQL và Redis.
   *   Tự động chạy các lệnh `migrate` để khởi tạo bảng dữ liệu.

---

## 🔒 Cơ chế xác thực (JWT Authentication)

Hệ thống sử dụng **JSON Web Token (JWT)** để bảo mật các API.

1.  **Lấy Token**: Gửi yêu cầu `POST` tới `/api/auth/jwt/create/` với `username` và `password`.
2.  **Sử dụng Token**: Đưa Access Token vào Header của các yêu cầu tiếp theo theo định dạng:
    ```text
    Authorization: Bearer <your_access_token>
    ```

---

## 📖 Tài liệu API (API Reference)

### 1. Auth Service (Port 8001)
**Authentication / Users**
* `POST /api/auth/users/`: Đăng ký tài khoản người dùng mới
* `POST /api/auth/jwt/create/`: Đăng nhập lấy cặp Token (Access & Refresh)
* `GET /api/auth/users/me/`: Lấy thông tin tài khoản hiện tại (🔒)
* `POST /api/auth/jwt/refresh/`: Làm mới Access Token
* `POST /api/auth/jwt/verify/`: Kiểm tra tính hợp lệ của Token

**Documentation**
* Swagger UI: [http://localhost:8001/swagger/](http://localhost:8001/swagger/)
* Redoc: [http://localhost:8001/redoc/](http://localhost:8001/redoc/)

### 2. Inventory Service (Port 8002)
**Catalog / Products**
* `GET /api/categories/`: Danh sách danh mục sản phẩm
* `POST /api/categories/`: Tạo danh mục mới (🔒)
* `GET /api/products/`: Danh sách toàn bộ sản phẩm (kèm tồn kho)
* `POST /api/products/`: Tạo sản phẩm mới (🔒)
* `GET /api/products/{id}/`: Chi tiết sản phẩm
* `PUT /api/products/{id}/`: Cập nhật thông tin sản phẩm (🔒)
* `DELETE /api/products/{id}/`: Xóa sản phẩm (🔒)

**Documentation**
* Swagger UI: [http://localhost:8002/swagger/](http://localhost:8002/swagger/)

### 3. Order Service (Port 8003)
**Cart**
* `GET /api/carts/`: Danh sách giỏ hàng
* `POST /api/carts/`: Tạo giỏ hàng mới
* `GET /api/carts/{id}/`: Chi tiết giỏ hàng và danh sách sản phẩm bên trong
* `DELETE /api/carts/{id}/`: Xóa giỏ hàng

**Orders**
* `GET /api/orders/`: Danh sách toàn bộ đơn hàng
* `POST /api/orders/`: Chốt đơn hàng (Tạo đơn hàng từ giỏ hàng và gửi Email báo về)
* `GET /api/orders/{id}/`: Chi tiết đơn hàng cụ thể

**Documentation**
* Swagger UI: [http://localhost:8003/swagger/](http://localhost:8003/swagger/)
