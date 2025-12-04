"""
Database connection for Vercel Serverless
Supabase PostgreSQL
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Supabase PostgreSQL URL (환경변수에서)
DATABASE_URL = os.environ.get("DATABASE_URL", "")

Base = declarative_base()

class GovernmentSupport(Base):
    """정부지원사업 공고"""
    __tablename__ = "government_supports"
    
    id = Column(Integer, primary_key=True)
    source_api = Column(String(20))
    title = Column(String(500))
    organization = Column(String(200))
    url = Column(String(1000), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# DB 엔진 및 세션
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
else:
    # 로컬 테스트용 SQLite
    engine = create_engine("sqlite:///./gov_support.db")
    SessionLocal = sessionmaker(bind=engine)

def get_db():
    """DB 세션 생성"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Serverless에서는 명시적으로 close
