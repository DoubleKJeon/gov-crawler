"""
간단한 데이터베이스 모델
minimal_test.py의 성공 패턴 사용
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GovernmentSupport(Base):
    """정부지원사업 공고 - 최소 필드만"""
    __tablename__ = "government_supports"
    
    id = Column(Integer, primary_key=True, index=True)
    source_api = Column(String(20), nullable=False, index=True)  # 'MSIT' or 'KSTARTUP'
    title = Column(String(500), nullable=False)
    organization = Column(String(200))
    url = Column(String(1000), unique=True)  # 중복 방지
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Support(id={self.id}, source={self.source_api}, title='{self.title[:30]}...')>"
