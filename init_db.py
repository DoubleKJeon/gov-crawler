"""
간단한 DB 초기화 스크립트
"""
import os
import sys

# 환경변수 설정
os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["SECRET_KEY"] = "test-secret"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"

from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# 모델 정의
class GovernmentSupport(Base):
    __tablename__ = "government_supports"
    id = Column(Integer, primary_key=True)
    source_api = Column(String(20))
    title = Column(String(500))
    organization = Column(String(200))
    category = Column(String(100))
    support_type = Column(String(100))
    target_audience = Column(Text)
    application_start_date = Column(Date)
    application_end_date = Column(Date)
    description = Column(Text)
    budget = Column(String(200))
    contact_info = Column(String(500))
    url = Column(String(1000))
    files = Column(JSON)
    is_new = Column(Boolean, default=True)
    first_crawled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    support_id = Column(Integer)
    memo = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationSetting(Base):
    __tablename__ = "notification_settings"
    user_id = Column(Integer, primary_key=True)
    email_enabled = Column(Boolean, default=True)
    notify_new_supports = Column(Boolean, default=True)
    notify_deadline = Column(Boolean, default=True)
    keywords = Column(JSON)
    categories = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow)

# DB 생성
print("데이터베이스 초기화 중...")
engine = create_engine("sqlite:///./gov_support.db")
Base.metadata.create_all(bind=engine)
print("✅ 데이터베이스 초기화 완료!")
