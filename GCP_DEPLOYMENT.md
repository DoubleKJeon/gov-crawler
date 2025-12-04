# GCP 배포 가이드

GCP Always Free Tier를 활용한 무료 배포 가이드입니다.

## 📋 사전 준비

### 1. GCP 계정
- Google Cloud Platform 계정 필요
- 결제 정보 등록 (무료 티어 사용 시 청구 없음)

### 2. Always Free 리소스
- **Compute Engine**: f1-micro 인스턴스 (us-west1, us-central1, us-east1)
- **디스크**: 30GB Standard persistent disk
- **네트워크**: 1GB 송신/월
- **Cloud Storage**: 5GB

---

## 🚀 배포 단계

### Step 1: GCP 프로젝트 생성

```bash
# Google Cloud Console에서
1. 새 프로젝트 생성
2. 프로젝트 ID 기록
```

### Step 2: Compute Engine 인스턴스 생성

**인스턴스 설정**:
- **머신 유형**: e2-micro (또는 f1-micro)
- **리전**: us-west1-b
- **부팅 디스크**: Ubuntu 22.04 LTS
- **디스크 크기**: 30GB
- **방화벽**: HTTP, HTTPS 트래픽 허용

**생성 명령어** (gcloud CLI):
```bash
gcloud compute instances create gov-crawler \
    --zone=us-west1-b \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --tags=http-server,https-server
```

### Step 3: 방화벽 규칙 설정

```bash
# 포트 8000 열기
gcloud compute firewall-rules create allow-gov-crawler \
    --allow=tcp:8000 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server
```

### Step 4: SSH 접속

```bash
gcloud compute ssh gov-crawler --zone=us-west1-b
```

### Step 5: 서버 설정

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.11 설치
sudo apt install -y python3.11 python3.11-venv python3-pip git

# 프로젝트 클론
git clone <your-repository-url>
cd Project4_정부지원사업_크롤러

# 가상환경 생성
python3.11 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
nano .env
# API 키 등 설정 입력
```

### Step 6: 데이터베이스 초기화

```bash
python -m app.database
```

### Step 7: systemd 서비스 설정

**서비스 파일 생성**:
```bash
sudo nano /etc/systemd/system/gov-crawler.service
```

**내용**:
```ini
[Unit]
Description=Government Support Crawler API
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/Project4_정부지원사업_크롤러
Environment="PATH=/home/your-username/Project4_정부지원사업_크롤러/venv/bin"
ExecStart=/home/your-username/Project4_정부지원사업_크롤러/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**서비스 활성화**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gov-crawler
sudo systemctl start gov-crawler
sudo systemctl status gov-crawler
```

### Step 8: Nginx 설정 (선택)

```bash
# Nginx 설치
sudo apt install -y nginx

# 설정 파일
sudo nano /etc/nginx/sites-available/gov-crawler
```

**Nginx 설정**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# 심볼릭 링크 생성
sudo ln -s /etc/nginx/sites-available/gov-crawler /etc/nginx/sites-enabled/

# Nginx 재시작
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 SSL 인증서 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt install -y certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com

# 자동 갱신 테스트
sudo certbot renew --dry-run
```

---

## 📊 모니터링

### 로그 확인

```bash
# 서비스 로그
sudo journalctl -u gov-crawler -f

# Nginx 로그
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# 애플리케이션 로그
tail -f logs/app.log
```

### 시스템 리소스

```bash
# CPU/메모리 사용량
htop

# 디스크 사용량
df -h

# 프로세스 확인
ps aux | grep uvicorn
```

---

## 🔄 업데이트 및 재배포

```bash
# 프로젝트 Pull
cd Project4_정부지원사업_크롤러
git pull

# 의존성 업데이트
source venv/bin/activate
pip install -r requirements.txt

# 서비스 재시작
sudo systemctl restart gov-crawler
```

---

## 💰 비용 최적화

### 1. 무료 티어 유지
- f1-micro 또는 e2-micro 사용
- us-west1, us-central1, us-east1 리전만
- 월 송신 1GB 이내 유지

### 2. SQLite 사용
- 별도 DB 서버 불필요
- 비용 절감

### 3. 스케줄러 최적화
- 크롤링 1일 1회로 제한
- 오프피크 시간 (자정) 실행

### 4. 로그 로테이션
```bash
# logrotate 설정
sudo nano /etc/logrotate.d/gov-crawler
```

**내용**:
```
/home/your-username/Project4_정부지원사업_크롤러/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 🐛 트러블슈팅

### 서비스가 시작되지 않는 경우

```bash
# 로그 확인
sudo journalctl -u gov-crawler -n 50

# 수동 실행으로 오류 확인
cd Project4_정부지원사업_크롤러
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 메모리 부족

```bash
# 스왑 파일 생성
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 포트가 이미 사용 중

```bash
# 포트 사용 확인
sudo lsof -i :8000

# 프로세스 종료
sudo kill -9 <PID>
```

---

## 📝 체크리스트

배포 전 확인사항:

- [ ] GCP 프로젝트 생성
- [ ] Compute Engine 인스턴스 생성
- [ ] 방화벽 규칙 설정
- [ ] SSH 접속 확인
- [ ] Python 및 의존성 설치
- [ ] 환경변수 설정 (.env)
- [ ] 데이터베이스 초기화
- [ ] systemd 서비스 등록
- [ ] 서비스 정상 작동 확인
- [ ] (선택) Nginx 설정
- [ ] (선택) SSL 인증서 발급
- [ ] 로그 모니터링 설정

---

## 🎯 배포 후 테스트

```bash
# 헬스 체크
curl http://your-server-ip:8000/health

# API 문서
http://your-server-ip:8000/docs

# 공고 목록
curl http://your-server-ip:8000/api/supports
```

---

**축하합니다! 서비스가 배포되었습니다! 🎉**
