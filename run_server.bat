@echo off
chcp 65001 > nul
echo ====================================
echo FastAPI 서버 실행
echo ====================================

REM 가상환경 활성화
call venv\Scripts\activate.bat

echo.
echo 서버 시작 중...
echo.
echo Swagger UI: http://localhost:8000/docs
echo ReDoc: http://localhost:8000/redoc
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
