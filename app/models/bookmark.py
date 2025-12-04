"""
북마크 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Bookmark(Base):
    """북마크"""
    
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    support_id = Column(Integer, ForeignKey("government_supports.id", ondelete="CASCADE"), nullable=False, index=True)
    memo = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="bookmarks")
    support = relationship("GovernmentSupport", back_populates="bookmarks")
    
    # 유니크 제약조건 (사용자당 공고 1개만 북마크)
    __table_args__ = (
        UniqueConstraint('user_id', 'support_id', name='uix_user_support'),
    )
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, support_id={self.support_id})>"
