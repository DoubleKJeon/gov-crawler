@echo off
chcp 65001 > nul
echo ====================================
echo 로컬 테스트 - 원스톱 실행
echo ====================================

REM 환경변수 설정
set MSIT_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
set KSTARTUP_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
set SECRET_KEY=test-secret-key-for-local-testing
set JWT_SECRET_KEY=test-jwt-secret-key-for-local
set DEBUG=True
set SCHEDULER_ENABLED=False
set EMAIL_ENABLED=False

echo [1/5] 가상환경 활성화...
call venv\Scripts\activate.bat

echo.
echo [2/5] 데이터베이스 초기화...
python -c "from sqlalchemy import create_engine; from sqlalchemy.ext.declarative import declarative_base; from app.models import GovernmentSupport, User, Bookmark, NotificationSetting; Base = declarative_base(); engine = create_engine('sqlite:///./gov_support.db'); Base.metadata.create_all(bind=engine); print('✓ DB 초기화 완료')"

echo.
echo [3/5] 크롤러 테스트...
echo.
python minimal_test.py

echo.
echo [4/5] 서버 시작 준비 완료!
echo.
echo ====================================
echo ✅ 로컬 환경 설정 완료!
echo ====================================
echo.
echo 다음 단계:
echo 1. 서버 실행: run_server.bat
echo 2. 브라우저에서: http://localhost:8000/docs
echo 3. API 테스트: run_tests.bat (새 터미널)
echo.
pause
