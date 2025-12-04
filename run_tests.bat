@echo off
chcp 65001 > nul
echo ====================================
echo API 테스트 실행
echo ====================================

echo.
echo 서버가 실행 중인지 확인하세요!
echo http://localhost:8000
echo.

REM 가상환경 활성화
call venv\Scripts\activate.bat

echo 테스트 시작...
echo.

python test_api.py

echo.
pause
