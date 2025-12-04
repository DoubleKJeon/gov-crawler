#!/bin/bash
# GCP 자동 배포 스크립트

set -e  # 오류 발생시 중단

echo "========================================="
echo "GCP 정부지원사업 크롤러 배포 스크립트"
echo "========================================="

# 변수 설정
PROJECT_ID="gov-support-crawler"  # 실제 프로젝트 ID로 변경
INSTANCE_NAME="gov-support-vm"
ZONE="asia-northeast3-a"
MACHINE_TYPE="e2-micro"

echo ""
echo "프로젝트 ID: $PROJECT_ID"
echo "인스턴스명: $INSTANCE_NAME"
echo "리전: $ZONE"
echo ""

# 1. 프로젝트 설정
echo "[1/8] 프로젝트 설정..."
gcloud config set project $PROJECT_ID

# 2. API 활성화
echo "[2/8] Compute Engine API 활성화..."
gcloud services enable compute.googleapis.com

# 3. VM 인스턴스 생성
echo "[3/8] VM 인스턴스 생성..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
apt update
apt install -y python3.11 python3.11-venv python3-pip
'

# 4. 방화벽 규칙 생성
echo "[4/8] 방화벽 규칙 생성..."

# 백엔드 포트 (8000)
gcloud compute firewall-rules create allow-crawler-backend \
    --allow=tcp:8000 \
    --target-tags=http-server \
    --description="Allow backend API access" \
    --direction=INGRESS || echo "이미 존재하는 규칙"

# 프론트엔드 포트 (3000)
gcloud compute firewall-rules create allow-crawler-frontend \
    --allow=tcp:3000 \
    --target-tags=http-server \
    --description="Allow frontend access" \
    --direction=INGRESS || echo "이미 존재하는 규칙"

# 5. VM 준비 대기
echo "[5/8] VM 부팅 대기 (30초)..."
sleep 30

# 6. 외부 IP 확인
echo "[6/8] VM 외부 IP 확인..."
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "외부 IP: $EXTERNAL_IP"

# 7. 파일 업로드
echo "[7/8] 프로젝트 파일 업로드..."
gcloud compute scp --recurse \
    --zone=$ZONE \
    simple_main.py \
    run_simple_crawler.py \
    simple_db_init.py \
    frontend/ \
    $INSTANCE_NAME:~/ || echo "파일 업로드 실패 - SSH로 수동 업로드 필요"

# 8. VM 설정 스크립트 실행
echo "[8/8] VM 내부 환경 설정..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
    # Python 가상환경 생성
    python3.11 -m venv venv
    source venv/bin/activate
    
    # 의존성 설치
    pip install fastapi uvicorn sqlalchemy requests python-multipart
    
    # DB 초기화
    python simple_db_init.py
    
    # Systemd 서비스 파일 생성
    echo "[Unit]
Description=Government Support Crawler Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
Environment=\"PATH=$HOME/venv/bin\"
ExecStart=$HOME/venv/bin/python simple_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gov-crawler-backend.service
    
    echo "[Unit]
Description=Government Support Crawler Frontend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/frontend
ExecStart=/usr/bin/python3 -m http.server 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gov-crawler-frontend.service
    
    # 서비스 시작
    sudo systemctl daemon-reload
    sudo systemctl enable gov-crawler-backend gov-crawler-frontend
    sudo systemctl start gov-crawler-backend gov-crawler-frontend
    
    # 상태 확인
    sudo systemctl status gov-crawler-backend --no-pager
    sudo systemctl status gov-crawler-frontend --no-pager
'

echo ""
echo "========================================="
echo "✅ 배포 완료!"
echo "========================================="
echo ""
echo "접속 정보:"
echo "  백엔드 API: http://$EXTERNAL_IP:8000/docs"
echo "  프론트엔드: http://$EXTERNAL_IP:3000"
echo ""
echo "SSH 접속:"
echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "로그 확인:"
echo "  sudo journalctl -u gov-crawler-backend -f"
echo "  sudo journalctl -u gov-crawler-frontend -f"
echo ""
