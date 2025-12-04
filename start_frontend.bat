@echo off
chcp 65001 > nul
echo ====================================
echo 프론트엔드 서버 시작
echo ====================================

cd frontend
echo.
echo 프론트엔드 서버를 시작합니다...
echo 브라우저에서 http://localhost:3000 으로 접속하세요!
echo.
echo Ctrl+C로 종료
echo.

python -m http.server 3000
