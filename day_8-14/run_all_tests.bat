@echo off
echo ======================================================
echo MICROSERVICES CI: LINTING AND QUALITY CHECK
echo ======================================================

echo.
echo [1/3] Quality Check: Auth Service...
docker-compose exec auth_service uv run ruff check .
docker-compose exec auth_service uv run pytest --cov=users --cov-report=term-missing

echo.
echo [2/3] Quality Check: Inventory Service...
docker-compose exec inventory_service uv run ruff check .
docker-compose exec inventory_service uv run pytest --cov=catalog --cov-report=term-missing

echo.
echo [3/3] Quality Check: Order Service...
docker-compose exec order_service uv run ruff check .
docker-compose exec order_service uv run pytest --cov=cart --cov=orders --cov-report=term-missing

echo.
echo ======================================================
echo CI FLOW COMPLETED
echo ======================================================
pause
