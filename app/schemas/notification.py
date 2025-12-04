"""
알림 설정 스키마
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class NotificationSettingBase(BaseModel):
    """알림 설정 기본"""
    email_enabled: bool = Field(True, description="이메일 알림 활성화")
    notify_new_supports: bool = Field(True, description="신규 공고 알림")
    notify_deadline: bool = Field(True, description="마감 임박 알림")
    keywords: Optional[List[str]] = Field(None, description="관심 키워드")
    categories: Optional[List[str]] = Field(None, description="관심 카테고리")


class NotificationSettingUpdate(NotificationSettingBase):
    """알림 설정 수정"""
    pass


class NotificationSettingResponse(NotificationSettingBase):
    """알림 설정 응답"""
    user_id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
