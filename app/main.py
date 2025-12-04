"""
FastAPI 메인 애플리케이션
"""
import os
import sys

# 환경변수 먼저 설정
os.environ.setdefault("MSIT_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("KSTARTUP_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("SCHEDULER_ENABLED", "False")

# config_simple을 config로 대체 (import 전에!)
from app import config_simple
sys.modules['app.config'] = config_simple

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db

# 스케줄러는 비활성화
# from app.utils.logger import setup_logger
# from app.utils.scheduler import scheduler

# 로거 초기화 (간단 버전)
# setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 생명주기 관리"""
    # 시작 시
    init_db()
    # scheduler.start()
    yield
    # 종료 시
    # scheduler.shutdown()


# FastAPI 앱
app = FastAPI(
    title="정부지원사업_크롤러",
    version="0.1.0",
    description="정부지원사업 정보 수집 및 검색 API",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "정부지원사업 크롤러 API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {
        "status": "healthy"
    }


# API 라우터 등록
from app.api import supports, auth, bookmarks, notifications

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(supports.router, prefix="/api", tags=["supports"])
app.include_router(bookmarks.router, prefix="/api", tags=["bookmarks"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])



if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("서버 시작 중...")
    print("=" * 60)
    print()
    print("📡 Swagger UI: http://localhost:8000/docs")
    print("📘 ReDoc: http://localhost:8000/redoc")
    print()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
