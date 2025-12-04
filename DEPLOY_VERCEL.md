# Supabase + Vercel 배포 가이드

## 🚀 빠른 시작

### 1. Supabase 설정 (5분)

#### 1.1 Supabase 가입 및 프로젝트 생성
1. https://supabase.com 접속
2. "Start your project" 클릭
3. GitHub 계정으로 로그인
4. "New Project" 클릭
5. **Database Password** 설정 및 저장 (중요!)
6. Region: **Northeast Asia (Seoul)** 선택
7. "Create new project" 클릭

#### 1.2 데이터베이스 테이블 생성
1. 프로젝트 대시보드 → **SQL Editor** 클릭
2. 다음 SQL 실행:

```sql
CREATE TABLE government_supports (
    id SERIAL PRIMARY KEY,
    source_api VARCHAR(20),
    title VARCHAR(500),
    organization VARCHAR(200),
    url VARCHAR(1000) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_source ON government_supports(source_api);
CREATE INDEX idx_created ON government_supports(created_at);
```

#### 1.3 Connection String 복사
1. Settings → Database
2. **Connection String** → **URI** 탭
3. `postgresql://postgres:[YOUR-PASSWORD]@...` 복사
4. `[YOUR-PASSWORD]`를 실제 비밀번호로 교체

---

### 2. GitHub 준비

```bash
# Git 저장소 확인
git status

# 변경사항 커밋
git add .
git commit -m "Add Vercel serverless deployment"
git push origin main
```

---

### 3. Vercel 배포 (5분)

#### 3.1 Vercel 가입 및 프로젝트 Import
1. https://vercel.com 접속
2. "Start Deploying" → GitHub로 로그인
3. "Import Git Repository"
4. 저장소 선택: `Project4_정부지원사업_크롤러`
5. "Import" 클릭

#### 3.2 환경 변수 설정
**Configure Project** 화면에서:

**Environment Variables** 추가:
```
DATABASE_URL = postgresql://postgres:...@...supabase.co:5432/postgres
MSIT_API_KEY = amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8=...
KSTARTUP_API_KEY = amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8=...
```

#### 3.3 배포
"Deploy" 버튼 클릭!

---

### 4. 배포 확인

배포 완료 후 (2~3분):
```
https://your-project.vercel.app
```

#### 4.1 API 테스트
```bash
# 통계 확인
curl https://your-project.vercel.app/api/stats

# 크롤러 실행
curl -X POST https://your-project.vercel.app/api/crawler

# 공고 조회
curl https://your-project.vercel.app/api/supports
```

---

## 🔄 자동 크롤링

**매일 오전 8시** 자동 실행 (vercel.json의 cron 설정)

수동 실행:
```bash
curl -X POST https://your-project.vercel.app/api/crawler
```

---

## 🛠️ 트러블슈팅

### 배포 실패
- Build Logs 확인
- 환경 변수 확인

### DB 연결 오류
- DATABASE_URL 확인
- Supabase에서 IP 허용 확인 (기본은 모두 허용)

### API 오류
- Vercel Functions 로그 확인
- API 키 확인

---

## 💰 비용

- **Supabase**: 무료 (500MB, 50만 요청/월)
- **Vercel**: 무료 (100GB 대역폭)
- **총**: **$0/월** ✅

---

## 📝 체크리스트

- [ ] Supabase 계정 생성
- [ ] 프로젝트 및 테이블 생성
- [ ] Connection String 복사
- [ ] GitHub Push
- [ ] Vercel Import
- [ ] 환경 변수 설정
- [ ] 배포 확인
- [ ] API 테스트

완료! 🎉
