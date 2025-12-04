# 로컬 테스트 가이드

## 1단계: 환경 설정 확인

### .env 파일 확인
```bash
# .env 파일이 있는지 확인
dir .env

# 없으면 생성
copy .env.example .env
```

**.env 파일에 필수 항목 입력**:
```
MSIT_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
KSTARTUP_API_KEY=amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

---

## 2단계: 데이터베이스 초기화

```bash
# 가상환경 활성화
venv\Scripts\activate

# DB 초기화
python -m app.database
```

**성공 메시지**:
```
✅ 데이터베이스 초기화 완료
```

---

## 3단계: 크롤러 테스트

```bash
# 최소 크롤러 테스트
python minimal_test.py
```

**예상 결과**:
```
[1/5] 데이터베이스 설정... ✓
[2/5] 과기부 API 호출...
  상태: 200
  수집: 10개
  ✓ 저장 완료
[3/5] K-Startup API 호출...
  상태: 200
  수집: 10개
  ✓ 저장 완료
[4/5] 수집된 데이터 확인...
  전체: 20개
  과기부: 10개
  K-Startup: 10개
[5/5] 샘플 데이터:
  출처: MSIT
  제목: ...
✅ 테스트 완료!
```

---

## 4단계: 서버 실행

### 방법 1: 배치 파일 (추천)
```bash
run_server.bat
```

### 방법 2: 직접 실행
```bash
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**성공 메시지**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 5단계: Swagger UI 확인

1. 브라우저 열기
2. `http://localhost:8000/docs` 접속
3. API 문서 확인

**확인 사항**:
- [ ] Swagger UI가 정상적으로 로드됨
- [ ] 4개 섹션 보임 (auth, supports, bookmarks, notifications)
- [ ] 각 섹션의 API 목록 확인

---

## 6단계: API 테스트

### 자동 테스트 실행

**새 터미널 열기** (서버는 계속 실행):
```bash
run_tests.bat
```

**예상 결과**:
```
[테스트] 헬스 체크
  상태: 200
  응답: {'status': 'healthy', ...}

[테스트] 인증 플로우
  1. 회원가입...
    상태: 201
  2. 로그인...
    상태: 200
    토큰: eyJhbGciOiJIUzI1NiI...
  3. 내 정보 조회...
    상태: 200
    이메일: test@example.com

[테스트] 공고 API
  1. 목록 조회...
    상태: 200
    전체: 20개
  2. 검색...
    상태: 200
  3. 신규 공고...
    상태: 200
    신규: 20개
  4. 통계...
    상태: 200
    전체: 20개
    과기부: 10개
    K-Startup: 10개

✅ 모든 테스트 통과!
```

---

## 7단계: 수동 API 테스트 (Swagger UI)

### 1. 회원가입
1. `POST /api/auth/register` 클릭
2. "Try it out" 클릭
3. 요청 본문:
```json
{
  "email": "test@local.com",
  "password": "test123456",
  "name": "테스트 사용자"
}
```
4. "Execute" 클릭
5. ✅ 응답: 201 Created

### 2. 로그인
1. `POST /api/auth/login` 클릭
2. "Try it out" 클릭
3. 요청 본문:
```json
{
  "email": "test@local.com",
  "password": "test123456"
}
```
4. "Execute" 클릭
5. ✅ 응답: 200 OK
6. **access_token 복사**

### 3. 인증 설정
1. 페이지 상단 "Authorize" 버튼 클릭
2. 입력란에 붙여넣기: `Bearer {access_token}`
3. "Authorize" 클릭
4. "Close" 클릭

### 4. 공고 조회
1. `GET /api/supports` 클릭
2. "Try it out" 클릭
3. page: 1, size: 10
4. "Execute" 클릭
5. ✅ 응답: 공고 목록

### 5. 북마크 추가 🔒
1. `POST /api/bookmarks` 클릭
2. "Try it out" 클릭
3. 요청 본문:
```json
{
  "support_id": 1,
  "memo": "관심있는 공고"
}
```
4. "Execute" 클릭
5. ✅ 응답: 201 Created

### 6. 내 북마크 조회 🔒
1. `GET /api/bookmarks` 클릭
2. "Try it out" 클릭
3. "Execute" 클릭
4. ✅ 응답: 북마크 목록

### 7. 알림 설정 변경 🔒
1. `PUT /api/notifications/settings` 클릭
2. "Try it out" 클릭
3. 요청 본문:
```json
{
  "email_enabled": true,
  "notify_new_supports": true,
  "notify_deadline": true,
  "keywords": ["AI", "스타트업"],
  "categories": ["창업지원"]
}
```
4. "Execute" 클릭
5. ✅ 응답: 200 OK

---

## 8단계: 수동 크롤링 테스트

### Swagger UI에서
1. `POST /api/crawler/run` 클릭
2. "Try it out" 클릭
3. "Execute" 클릭
4. ✅ 응답: 크롤링 결과

### 결과 확인
```json
{
  "success": true,
  "message": "크롤링 완료",
  "results": [
    {
      "source": "MSIT",
      "fetched": 10,
      "saved": 5
    },
    {
      "source": "KSTARTUP",
      "fetched": 10,
      "saved": 5
    }
  ]
}
```

---

## 체크리스트

### 필수 확인 사항
- [ ] .env 파일 설정 완료
- [ ] 데이터베이스 초기화 성공
- [ ] 크롤러 테스트 통과
- [ ] 서버 정상 실행
- [ ] Swagger UI 접속 성공
- [ ] 자동 API 테스트 통과
- [ ] 회원가입/로그인 성공
- [ ] 공고 조회 성공
- [ ] 북마크 추가/조회 성공
- [ ] 수동 크롤링 성공

### 선택 확인 사항
- [ ] 검색 기능 테스트
- [ ] 필터링 테스트
- [ ] 통계 API 테스트
- [ ] 알림 설정 변경 테스트

---

## 문제 발생 시

### 서버가 시작되지 않음
```bash
# 포트 사용 확인
netstat -ano | findstr :8000

# 프로세스 종료
taskkill /PID <PID> /F
```

### API 키 오류
```
# .env 파일 확인
type .env

# API 키 재확인
```

### 크롤러 오류
```bash
# 직접 테스트
python minimal_test.py
```

### 데이터베이스 오류
```bash
# DB 재초기화
del /f gov_support.db
python -m app.database
```

---

## 다음 단계

모든 테스트 통과 후:
1. ✅ **로컬 테스트 완료**
2. 🚀 **GCP 배포 준비**
3. 📦 **프로젝트 코드 정리**
4. 🌐 **클라우드 배포**

---

**문제가 생기면 언제든지 말씀하세요!**
