"""
알림 설정 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class NotificationSetting(Base):
    """알림 설정"""
    
    __tablename__ = "notification_settings"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # 알림 활성화
    email_enabled = Column(Boolean, default=True)
    notify_new_supports = Column(Boolean, default=True)
    notify_deadline = Column(Boolean, default=True)
    
    # 필터 (JSON 배열)
    keywords = Column(JSON)  # ["스타트업", "AI"]
    categories = Column(JSON)  # ["창업지원", "R&D"]
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="notification_setting")
    
    def __repr__(self):
        return f"<NotificationSetting(user_id={self.user_id}, email_enabled={self.email_enabled})>"
