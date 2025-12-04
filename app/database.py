"""
간단한 데이터베이스 연결
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 환경변수 설정 (Windows .env 문제 회피)
os.environ.setdefault("MSIT_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("KSTARTUP_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./gov_support.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite용
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """DB 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
