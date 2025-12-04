@echo off
echo ============================================
echo 정부지원사업 크롤러 설치 및 테스트
echo ============================================

REM 가상환경 생성
echo.
echo [1/6] 가상환경 생성...
if not exist venv (
    python -m venv venv
    echo ✓ 가상환경 생성 완료
) else (
    echo ✓ 가상환경이 이미 존재합니다
)

REM 가상환경 활성화
echo.
echo [2/6] 가상환경 활성화...
call venv\Scripts\activate.bat

REM 의존성 설치
echo.
echo [3/6] 의존성 설치...
pip install -r requirements.txt

REM 환경변수 파일 생성
echo.
echo [4/6] 환경변수 파일 설정...
if not exist .env (
    copy .env.example .env
    echo ✓ .env 파일 생성 완료
    echo.
    echo ⚠️  .env 파일을 열어서 API 키를 입력하세요!
    echo     - MSIT_API_KEY
    echo     - KSTARTUP_API_KEY
    echo.
    pause
) else (
    echo ✓ .env 파일이 이미 존재합니다
)

REM 데이터베이스 초기화
echo.
echo [5/6] 데이터베이스 초기화...
python -m app.database

REM 크롤러 테스트
echo.
echo [6/6] 크롤러 테스트 실행...
echo.
python test_crawler.py

echo.
echo ============================================
echo 설치 및 테스트 완료!
echo ============================================
echo.
echo 서버 실행: uvicorn app.main:app --reload
echo.
pause
