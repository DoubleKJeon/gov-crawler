"""
정부지원사업 공고 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, JSON, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class GovernmentSupport(Base):
    """정부지원사업 공고"""
    
    __tablename__ = "government_supports"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # 출처
    source_api = Column(String(20), nullable=False, index=True)  # 'MSIT' or 'KSTARTUP'
    
    # 기본 정보
    title = Column(String(500), nullable=False, index=True)
    organization = Column(String(200))
    category = Column(String(100), index=True)
    support_type = Column(String(100))
    target_audience = Column(Text)
    
    # 일정
    application_start_date = Column(Date, index=True)
    application_end_date = Column(Date, index=True)
    
    # 상세 정보
    description = Column(Text)
    budget = Column(String(200))
    contact_info = Column(String(500))
    url = Column(String(1000))
    files = Column(JSON)  # 첨부파일 정보 (배열)
    
    # 신규 추적
    is_new = Column(Boolean, default=True, index=True)
    first_crawled_at = Column(DateTime, default=datetime.utcnow)
    
    # 메타데이터
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    bookmarks = relationship("Bookmark", back_populates="support", cascade="all, delete-orphan")
    
    # 유니크 제약조건 (출처 + URL)
    __table_args__ = (
        UniqueConstraint('source_api', 'url', name='uix_source_url'),
    )
    
    def __repr__(self):
        return f"<GovernmentSupport(id={self.id}, title='{self.title[:30]}...')>"
