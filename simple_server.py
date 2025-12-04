"""
간단한 테스트 서버
"""
import os
import sys

# 환경변수 설정
os.environ.setdefault("MSIT_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("KSTARTUP_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("SCHEDULER_ENABLED", "False")
os.environ.setdefault("EMAIL_ENABLED", "False")  
os.environ.setdefault("REDIS_ENABLED", "False")

# config_simple을 config로 대체
from app import config_simple
sys.modules['app.config'] = config_simple

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("=" * 60)
print("서버 초기화 중...")
print("=" * 60)

# FastAPI 앱
app = FastAPI(
    title="정부지원사업_크롤러",
    version="0.1.0",
    description="정부지원사업 정보 수집 및 검색 API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "정부지원사업 크롤러 API", 
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# API 라우터 등록
try:
    from app.api import supports, auth, bookmarks, notifications
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(supports.router, prefix="/api", tags=["supports"])
    app.include_router(bookmarks.router, prefix="/api", tags=["bookmarks"])
    app.include_router(notifications.router, prefix="/api", tags=["notifications"])
    print("✅ API 라우터 등록 완료")
except Exception as e:
    print(f"⚠️ API 라우터 등록 실패: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
print("서버 준비 완료!")
print()  
print("📡 Swagger UI: http://localhost:8000/docs")
print("📘 ReDoc: http://localhost:8000/redoc")
print()
print("Ctrl+C로 종료")
print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
