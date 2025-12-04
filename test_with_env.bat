@echo off
chcp 65001 > nul
echo ====================================
echo 크롤러 테스트 (환경변수 방식)
echo ====================================

REM 환경변수 설정
set MSIT_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
set KSTARTUP_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
set LOG_LEVEL=INFO
set DATABASE_URL=sqlite:///./gov_support.db
set DEBUG=True
set SCHEDULER_ENABLED=False

echo [1/2] 가상환경 활성화...
call venv\Scripts\activate.bat

echo.
echo [2/2] 크롤러 테스트 실행...
echo.
python simple_test_crawler.py

echo.
echo ====================================
echo 테스트 완료!
echo ====================================
pause
