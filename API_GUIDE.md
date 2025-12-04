# API 사용 가이드

FastAPI로 제공되는 RESTful API 사용법입니다.

## 🌐 Swagger UI

가장 쉬운 방법:
```
http://localhost:8000/docs
```

모든 API를 웹 브라우저에서 직접 테스트할 수 있습니다.

---

## 🔐 인증

대부분의 API는 JWT 토큰이 필요합니다.

### 1. 회원가입

```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "홍길동"
}
```

**응답**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "last_login": null
}
```

### 2. 로그인

```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**응답**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 인증이 필요한 API 호출

```bash
GET /api/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📋 공고 조회

### 목록 조회

```bash
GET /api/supports?page=1&size=20

# 응답
{
  "total": 150,
  "page": 1,
  "size": 20,
  "items": [...]
}
```

### 상세 조회

```bash
GET /api/supports/123
```

### 신규 공고만

```bash
GET /api/supports/new?page=1&size=10
```

### 검색

```bash
# 키워드 검색
GET /api/supports/search?keyword=스타트업

# 카테고리 필터
GET /api/supports/search?category=창업지원

# 기관 필터
GET /api/supports/search?organization=과학기술정보통신부

# 진행 상태
GET /api/supports/search?status=ongoing
# status: ongoing (진행중), upcoming (예정), closed (마감)

# 복합 검색
GET /api/supports/search?keyword=AI&category=R%26D&status=ongoing
```

---

## ⭐ 북마크

### 추가 🔒

```bash
POST /api/bookmarks
Authorization: Bearer {token}
Content-Type: application/json

{
  "support_id": 123,
  "memo": "내년에 신청하기"
}
```

### 목록 🔒

```bash
GET /api/bookmarks
Authorization: Bearer {token}
```

### 수정 🔒

```bash
PUT /api/bookmarks/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "memo": "다음 달에 신청"
}
```

### 삭제 🔒

```bash
DELETE /api/bookmarks/1
Authorization: Bearer {token}
```

---

## 🔔 알림 설정

### 조회 🔒

```bash
GET /api/notifications/settings
Authorization: Bearer {token}
```

### 변경 🔒

```bash
PUT /api/notifications/settings
Authorization: Bearer {token}
Content-Type: application/json

{
  "email_enabled": true,
  "notify_new_supports": true,
  "notify_deadline": true,
  "keywords": ["AI", "스타트업", "R&D"],
  "categories": ["창업지원", "R&D"]
}
```

---

## 📊 통계

```bash
GET /api/stats

# 응답
{
  "total_supports": 150,
  "new_supports": 5,
  "msit_supports": 80,
  "kstartup_supports": 70,
  "ongoing_supports": 30,
  "upcoming_supports": 50,
  "closed_supports": 70
}
```

---

## 🛠️ 관리

### 수동 크롤링

```bash
POST /api/crawler/run
```

자동 스케줄링이 있지만, 필요 시 수동으로 크롤링을 실행할 수 있습니다.

---

## 💡 예제 시나리오

### 시나리오 1: 신규 사용자

```bash
# 1. 회원가입
POST /api/auth/register
{"email": "user@example.com", "password": "test123"}

# 2. 로그인
POST /api/auth/login
{"email": "user@example.com", "password": "test123"}
# → 토큰 획득

# 3. 공고 검색
GET /api/supports/search?keyword=스타트업&status=ongoing

# 4. 관심 공고 북마크
POST /api/bookmarks
{"support_id": 123, "memo": "관심있음"}

# 5. 알림 설정
PUT /api/notifications/settings
{"keywords": ["스타트업", "AI"], "categories": ["창업지원"]}
```

### 시나리오 2: 마감 임박 공고 찾기

```bash
# 진행 중인 공고 검색
GET /api/supports/search?status=ongoing

# 북마크한 공고 확인
GET /api/bookmarks

# → 마감 임박 시 자동으로 이메일 알림 수신
```

---

## 🔍 필터링 옵션

### 공고 목록/검색 공통

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `page` | 페이지 번호 | `1` |
| `size` | 페이지 크기 (최대 100) | `20` |

### 검색 전용

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `keyword` | 키워드 (제목+내용) | `스타트업` |
| `category` | 카테고리 | `창업지원` |
| `organization` | 기관명 | `과기부` |
| `status` | 진행 상태 | `ongoing`, `upcoming`, `closed` |

---

## 📝 응답 형식

### 성공

```json
{
  "id": 123,
  "title": "공고 제목",
  ...
}
```

### 오류

```json
{
  "detail": "오류 메시지"
}
```

### HTTP 상태 코드

- `200`: 성공
- `201`: 생성 성공
- `204`: 삭제 성공 (응답 없음)
- `400`: 잘못된 요청
- `401`: 인증 필요
- `403`: 권한 없음
- `404`: 찾을 수 없음
- `500`: 서버 오류

---

## 🧪 테스트

### Python

```python
import requests

# 로그인
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "user@example.com", "password": "test123"}
)
token = response.json()["access_token"]

# 인증 필요한 API
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/bookmarks",
    headers=headers
)
print(response.json())
```

### cURL

```bash
# 로그인
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"test123"}' \
  | jq -r '.access_token')

# 북마크 조회
curl "http://localhost:8000/api/bookmarks" \
  -H "Authorization: Bearer $TOKEN"
```

### JavaScript (fetch)

```javascript
// 로그인
const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'test123'
  })
});
const {access_token} = await response.json();

// 북마크 조회
const bookmarks = await fetch('http://localhost:8000/api/bookmarks', {
  headers: {'Authorization': `Bearer ${access_token}`}
}).then(r => r.json());
```

---

**더 많은 예제는 Swagger UI (`/docs`)에서 확인하세요!**
