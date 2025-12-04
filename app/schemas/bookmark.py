"""
북마크 스키마
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BookmarkBase(BaseModel):
    """북마크 기본 스키마"""
    support_id: int = Field(..., description="공고 ID")
    memo: Optional[str] = Field(None, description="메모")


class BookmarkCreate(BookmarkBase):
    """북마크 생성"""
    pass


class BookmarkUpdate(BaseModel):
    """북마크 수정"""
    memo: Optional[str] = Field(None, description="메모")


class BookmarkResponse(BookmarkBase):
    """북마크 응답"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# BookmarkWith Support는 나중에 사용
# class BookmarkWithSupport(BookmarkResponse):
    # """북마크 + 공고 정보"""
   # support: Any
