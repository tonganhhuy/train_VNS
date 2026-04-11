@echo off
echo Starting Microservices E-Commerce System...

REM Bật Redis lên trước nếu dùng docker, ở đây yêu cầu bạn đã cài redis/chạy qua docker redis 
REM Nếu không có redis thì Celery sẽ báo lỗi connection

cd auth_service
start "Auth Service" cmd /c "python manage.py runserver 8001"
cd ..

cd inventory_service
start "Inventory Service" cmd /c "python manage.py runserver 8002"
cd ..

cd order_service
start "Order Service" cmd /c "python manage.py runserver 8003"
start "Celery Worker" cmd /c "celery -A order_service worker -l info --pool=solo"
cd ..

echo Toan bo cac services da duoc khoi dong tren cac tabs cmd moi!
