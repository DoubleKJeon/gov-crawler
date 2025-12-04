# GCP 배포 빠른 가이드

## 현재 상태
✅ 로컬 테스트 완료  
✅ 모든 기능 정상 작동  
✅ 배포 파일 준비 완료

## 🚀 배포 3단계

### 1단계: GCP 인스턴스 생성 (5분)

**GCP Console에서**:
1. Compute Engine → VM instances
2. Create Instance 클릭
3. 설정:
   - Name: `gov-crawler`
   - Region: `us-west1` (Always Free)
   - Machine type: `e2-micro` (Always Free)
   - Boot disk: Ubuntu 22.04 LTS, 30GB
   - Firewall: ✓ HTTP, ✓ HTTPS
4. CREATE 클릭

**또는 gcloud CLI**:
```bash
gcloud compute instances create gov-crawler \
  --zone=us-west1-b \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB \
  --tags=http-server,https-server
```

### 2단계: 방화벽 설정 (2분)

```bash
# 포트 8000 열기
gcloud compute firewall-rules create allow-gov-crawler \
  --allow=tcp:8000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server
```

### 3단계: 코드 배포 (10분)

#### 방법 A: GitHub 사용 (추천)
```bash
# 1. SSH 접속
gcloud compute ssh gov-crawler --zone=us-west1-b

# 2. 코드 clone
git clone https://github.com/YOUR_USERNAME/Project4_정부지원사업_크롤러.git
cd Project4_정부지원사업_크롤러

# 3. API 키 설정
export MSIT_API_KEY="your_api_key"
export KSTARTUP_API_KEY="your_api_key"

# 4. 자동 설치 실행
chmod +x deploy/install_gcp.sh
./deploy/install_gcp.sh
```

#### 방법 B: 직접 업로드
```bash
# 로컬에서 실행
gcloud compute scp --recurse \
  d:\Antigravity\Project4_정부지원사업_크롤러 \
  gov-crawler:~ \
  --zone=us-west1-b

# 그 다음 SSH 접속 후 install_gcp.sh 실행
```

## ✅ 완료 확인

배포 후 확인:
```bash
# 인스턴스 외부 IP 확인
gcloud compute instances list

# 브라우저에서 접속
http://YOUR_EXTERNAL_IP:8000/docs
```

## 📝 배포 전 체크리스트

- [ ] GCP 계정 있음
- [ ] 프로젝트 생성됨
- [ ] API 키 준비됨
- [ ] (선택) GitHub 저장소 설정
- [ ] (선택) gcloud CLI 설치

## 🆘 문제 해결

### 서비스가 안 뜨는 경우
```bash
sudo systemctl status gov-crawler
sudo journalctl -u gov-crawler -n 50
```

### 포트 접근 안 되는 경우
```bash
# 방화벽 확인
gcloud compute firewall-rules list
sudo ufw status
```

---

**준비되셨으면 시작하세요!**

가장 쉬운 방법:
1. GCP Console에서 인스턴스 생성
2. SSH 접속
3. 이 저장소 clone 또는 업로드
4. `./deploy/install_gcp.sh` 실행

끝! 🎉
