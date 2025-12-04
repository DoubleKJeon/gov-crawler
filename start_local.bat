@echo off
chcp 65001 > nul
echo ====================================
echo 서버 시작 중...
echo ====================================
echo.

venv\Scripts\python.exe simple_server.py
