#!/bin/bash

# GCP 서버 자동 설치 스크립트
# Ubuntu 22.04 LTS 기준

set -e

echo "======================================"
echo "정부지원사업 크롤러 설치 시작"
echo "======================================"

# 1. 시스템 업데이트
echo "[1/8] 시스템 업데이트..."
sudo apt update && sudo apt upgrade -y

# 2. Python 3.11 설치
echo "[2/8] Python 3.11 설치..."
sudo apt install -y python3.11 python3.11-venv python3-pip git

# 3. 프로젝트 디렉토리로 이동 (이미 clone되어 있다고 가정)
cd ~/Project4_정부지원사업_크롤러

# 4. 가상환경 생성
echo "[3/8] 가상환경 생성..."
python3.11 -m venv venv

# 5. 의존성 설치
echo "[4/8] 의존성 설치..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. 환경변수 설정
echo "[5/8] 환경변수 설정..."
cat > .env.production << EOF
MSIT_API_KEY=${MSIT_API_KEY}
KSTARTUP_API_KEY=${KSTARTUP_API_KEY}
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
SCHEDULER_ENABLED=True
EMAIL_ENABLED=False
REDIS_ENABLED=False
EOF

# 7. 데이터베이스 초기화
echo "[6/8] 데이터베이스 초기화..."
python init_db.py

# 8. systemd 서비스 설정
echo "[7/8] systemd 서비스 설정..."
sudo cp deploy/gov-crawler.service /etc/systemd/system/
sudo sed -i "s/YOUR_USERNAME/$USER/g" /etc/systemd/system/gov-crawler.service
sudo systemctl daemon-reload
sudo systemctl enable gov-crawler
sudo systemctl start gov-crawler

# 9. 상태 확인
echo "[8/8] 서비스 상태 확인..."
sudo systemctl status gov-crawler

echo ""
echo "======================================"
echo "✅ 설치 완료!"
echo "======================================"
echo ""
echo "서비스 상태: sudo systemctl status gov-crawler"
echo "로그 확인: sudo journalctl -u gov-crawler -f"
echo "API 주소: http://$(curl -s ifconfig.me):8000"
echo "Swagger UI: http://$(curl -s ifconfig.me):8000/docs"
echo ""
