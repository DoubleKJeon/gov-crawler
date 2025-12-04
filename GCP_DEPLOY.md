# GCP 배포 가이드

## 🚀 GCP 배포 단계

### 1. 사전 준비 (사용자 직접 수행)

#### ✅ GCP 콘솔에서 설정
1. **프로젝트 생성/선택**
   - https://console.cloud.google.com
   - 프로젝트 ID 메모 (예: `gov-support-crawler`)

2. **결제 계정 연결**
   - 프로젝트에 결제 계정 연결 필요

3. **API 활성화**
   - Compute Engine API 활성화
   - 또는 아래 gcloud 명령어로 자동 활성화

#### ✅ 로컬에서 gcloud CLI 설치 및 인증
```bash
# gcloud CLI 설치 여부 확인
gcloud --version

# 설치 안되어 있으면: https://cloud.google.com/sdk/docs/install

# 인증
gcloud auth login

# 프로젝트 설정
gcloud config set project [YOUR_PROJECT_ID]
```

---

### 2. VM 인스턴스 생성 (CLI 자동화)

```bash
# Compute Engine API 활성화
gcloud services enable compute.googleapis.com

# VM 인스턴스 생성
gcloud compute instances create gov-support-vm \
    --zone=asia-northeast3-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server

# 방화벽 규칙 생성 (포트 8000, 3000 오픈)
gcloud compute firewall-rules create allow-crawler-backend \
    --allow=tcp:8000 \
    --target-tags=http-server \
    --description="Allow backend API access"

gcloud compute firewall-rules create allow-crawler-frontend \
    --allow=tcp:3000 \
    --target-tags=http-server \
    --description="Allow frontend access"
```

---

### 3. VM에 접속 및 환경 설정

```bash
# SSH 접속
gcloud compute ssh gov-support-vm --zone=asia-northeast3-a

# 이후 VM 내부에서 실행
```

#### VM 내부에서:

```bash
# 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.11 설치
sudo apt install -y python3.11 python3.11-venv python3-pip git

# 프로젝트 클론 (또는 파일 업로드)
git clone [YOUR_REPO_URL]
# 또는
# gcloud compute scp를 사용해서 파일 업로드

cd Project4_정부지원사업_크롤러

# 가상환경 생성
python3.11 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install fastapi uvicorn sqlalchemy requests python-multipart

# DB 초기화
python simple_db_init.py
```

---

### 4. Systemd 서비스 설정

#### 백엔드 서비스 (`/etc/systemd/system/gov-crawler-backend.service`):

```ini
[Unit]
Description=Government Support Crawler Backend
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Project4_정부지원사업_크롤러
Environment="PATH=/home/YOUR_USERNAME/Project4_정부지원사업_크롤러/venv/bin"
ExecStart=/home/YOUR_USERNAME/Project4_정부지원사업_크롤러/venv/bin/python simple_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 프론트엔드 서비스 (`/etc/systemd/system/gov-crawler-frontend.service`):

```ini
[Unit]
Description=Government Support Crawler Frontend
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Project4_정부지원사업_크롤러/frontend
ExecStart=/usr/bin/python3 -m http.server 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 서비스 시작:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gov-crawler-backend
sudo systemctl enable gov-crawler-frontend
sudo systemctl start gov-crawler-backend
sudo systemctl start gov-crawler-frontend

# 상태 확인
sudo systemctl status gov-crawler-backend
sudo systemctl status gov-crawler-frontend
```

---

### 5. 외부 IP 확인 및 접속

```bash
# VM 외부 IP 확인
gcloud compute instances describe gov-support-vm \
    --zone=asia-northeast3-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

**접속**:
- 백엔드 API: `http://[EXTERNAL_IP]:8000/docs`
- 프론트엔드: `http://[EXTERNAL_IP]:3000`

---

### 6. 크롤러 실행

```bash
# SSH로 접속 후
curl -X POST http://localhost:8000/api/crawler/run

# 또는 외부에서
curl -X POST http://[EXTERNAL_IP]:8000/api/crawler/run
```

---

### 7. Cron 설정 (자동 크롤링)

```bash
# crontab 편집
crontab -e

# 매일 오전 8시 크롤링
0 8 * * * curl -X POST http://localhost:8000/api/crawler/run
```

---

## 🔧 자동 배포 스크립트

위의 모든 단계를 자동화한 스크립트는 `deploy_gcp.sh` 참조

---

## 📊 모니터링

```bash
# 로그 확인
sudo journalctl -u gov-crawler-backend -f
sudo journalctl -u gov-crawler-frontend -f

# 리소스 사용량
htop
df -h
```

---

## 🛠️ 트러블슈팅

### VM 접속 안됨
```bash
gcloud compute ssh gov-support-vm --zone=asia-northeast3-a --troubleshoot
```

### 서비스 재시작
```bash
sudo systemctl restart gov-crawler-backend
sudo systemctl restart gov-crawler-frontend
```

### 방화벽 확인
```bash
gcloud compute firewall-rules list
```

---

## 💰 비용 절감

**e2-micro 인스턴스**: 무료 티어 포함 (매월 ~$7)

**비용 절감 방법**:
1. 사용하지 않을 때 VM 중지: `gcloud compute instances stop gov-support-vm --zone=asia-northeast3-a`
2. 예약된 인스턴스 사용
3. 스토리지 정리

---

## 🔐 보안

1. **방화벽**: 필요한 포트만 오픈
2. **SSH 키**: gcloud SSH 사용 (자동 관리)
3. **정기 업데이트**: `sudo apt update && sudo apt upgrade`

---

## ✅ 체크리스트

- [ ] GCP 프로젝트 생성
- [ ] gcloud CLI 설치 및 인증
- [ ] Compute Engine API 활성화
- [ ] VM 인스턴스 생성
- [ ] 방화벽 규칙 설정
- [ ] SSH 접속 확인
- [ ] Python 및 의존성 설치
- [ ] 코드 배포
- [ ] Systemd 서비스 설정
- [ ] 외부 접속 확인
- [ ] 크롤러 테스트
- [ ] Cron 설정

완료!
