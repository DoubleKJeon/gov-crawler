# 정부지원사업 크롤러 베타 서비스 - 최종 완성! 🎉

정부지원사업 정보를 자동 수집하고 사용자에게 맞춤 알림을 제공하는 완전한 백엔드 시스템입니다.

## 🌟 주요 기능

### 데이터 수집
- ✅ **과기부 + K-Startup** API 통합
- ✅ 자동 크롤링 (매일 자정)
- ✅ 신규 공고 자동 추적
- ✅ 중복 방지

### 사용자 시스템
- ✅ JWT 기반 인증
- ✅ 회원가입/로그인
- ✅ 프로필 관리

### 북마크 & 알림
- ✅ 관심 공고 북마크
- ✅ 메모 기능
- ✅ 이메일 알림 (신규/마감임박)
- ✅ 맞춤 알림 설정

### 검색 & 필터
- ✅ 키워드 검색
- ✅ 카테고리/기관/상태 필터
- ✅ 페이지네이션
- ✅ 통계

## 📡 API 엔드포인트 (20+)

### 인증 (`/api/auth`)
```
POST   /register       회원가입
POST   /login         로그인
GET    /me           내 정보 🔒
PUT    /me           정보 수정 🔒
DELETE /me           회원 탈퇴 🔒
```

### 공고 (`/api/supports`)
```
GET  /supports              목록
GET  /supports/new          신규 공고
GET  /supports/search       검색
GET  /supports/{id}         상세
GET  /stats                통계
POST /crawler/run          수동 크롤링
```

### 북마크 (`/api/bookmarks`)
```
POST   /bookmarks         추가 🔒
GET    /bookmarks         목록 🔒
PUT    /bookmarks/{id}    수정 🔒
DELETE /bookmarks/{id}   삭제 🔒
```

### 알림 (`/api/notifications`)
```
GET /settings    조회 🔒
PUT /settings    변경 🔒
```

🔒 = 인증 필요 (Bearer Token)

## 🚀 빠른 시작

### 1. 설치
```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
copy .env.example .env
# .env 파일에 API 키 입력
```

### 2. 실행
```bash
# 서버 시작
run_server.bat

# 또는
uvicorn app.main:app --reload
```

### 3. 테스트
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ 기술 스택

- **Framework**: FastAPI 0.104+
- **Database**: SQLAlchemy + SQLite
- **Auth**: JWT (python-jose) + bcrypt
- **Schedule**: APScheduler
- **Email**: SMTP
- **Docs**: OpenAPI 3.0 (자동 생성)

## 📁 프로젝트 구조

```
app/
├── api/           API 라우터
│   ├── auth.py
│   ├── supports.py
│   ├── bookmarks.py
│   └── notifications.py
├── models/        DB 모델
├── schemas/       Pydantic 스키마
├── crawlers/      크롤러
├── services/      비즈니스 로직
├── utils/         유틸리티
├── config.py      설정
├── database.py    DB 연결
└── main.py        FastAPI 앱
```

## 🔧 설정

`.env` 파일 예시:
```bash
# API Keys
MSIT_API_KEY=your_api_key
KSTARTUP_API_KEY=your_api_key

# JWT
JWT_SECRET_KEY=your_secret_key

# Email (선택)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email
SMTP_PASSWORD=your_password
EMAIL_ENABLED=True

# Scheduler
SCHEDULER_ENABLED=True
CRAWLER_CRON=0 0 * * *
```

## 🎯 사용 예시

### 1. 회원가입 & 로그인
```bash
# 회원가입
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### 2. 공고 검색
```bash
# 키워드 검색
GET /api/supports/search?keyword=스타트업&status=ongoing

# 신규 공고
GET /api/supports/new
```

### 3. 북마크 & 알림
```bash
# 북마크 추가
POST /api/bookmarks
{
  "support_id": 123,
  "memo": "내년에 신청하기"
}

# 알림 설정
PUT /api/notifications/settings
{
  "email_enabled": true,
  "keywords": ["AI", "스타트업"],
  "categories": ["창업지원"]
}
```

## 📊 데이터베이스

**4개 테이블**:
- `government_supports` - 공고 정보
- `users` - 사용자
- `bookmarks` - 북마크
- `notification_settings` - 알림 설정

**자동 관계 관리**:
- 사용자 삭제 시 북마크/알림 자동 삭제 (CASCADE)
- 공고 중복 방지 (source_api + url UNIQUE)

## 🔐 보안

- ✅ bcrypt 비밀번호 해싱
- ✅ JWT 토큰 인증
- ✅ CORS 설정
- ✅ SQL Injection 방지 (ORM)
- ✅ 환경변수 관리

## 🧪 테스트

```bash
# 최소 테스트
python minimal_test.py

# 서버 테스트
# Swagger UI에서 직접 테스트
```

## 📈 성능

- **페이지네이션**: 대용량 데이터 지원
- **인덱스**: 주요 필드 최적화
- **캐싱**: Redis 지원 (선택)

## 🌐 배포

### GCP Always Free Tier
```bash
# f1-micro 인스턴스에 배포 가능
# 월 트래픽 제한 내 무료 운영
```

자세한 내용은 `implementation_plan.md` 참고

## 📝 라이선스

MIT License

## 📚 문서

- **[README.md](README.md)** - 기본 사용 가이드
- **[API_GUIDE.md](API_GUIDE.md)** - API 사용법 및 예제
- **[GCP_DEPLOYMENT.md](GCP_DEPLOYMENT.md)** - GCP 배포 가이드
- **[COMPLETED.md](COMPLETED.md)** - 개발 완료 요약
- **Swagger UI** - http://localhost:8000/docs (서버 실행 후)

## 🔗 빠른 링크

| 기능 | 설명 | 링크 |
|------|------|------|
| 🚀 빠른 시작 | 설치 및 실행 | [바로가기](#-빠른-시작) |
| 📡 API 사용법 | 전체 API 가이드 | [API_GUIDE.md](API_GUIDE.md) |
| 🌐 배포 | GCP 무료 배포 | [GCP_DEPLOYMENT.md](GCP_DEPLOYMENT.md) |
| 🧪 테스트 | API 테스트 실행 | `run_tests.bat` |
| 📊 Swagger | API 문서 및 테스트 | http://localhost:8000/docs |

## 🙏 감사

- 공공데이터포털 (data.go.kr)
- FastAPI 커뮤니티

---

**Made with ❤️ using FastAPI**
