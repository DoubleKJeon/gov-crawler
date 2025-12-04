"""
정부지원사업 스키마
"""
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field


class GovernmentSupportBase(BaseModel):
    """기본 공고 스키마"""
    title: str = Field(..., description="공고 제목")
    organization: Optional[str] = Field(None, description="담당 기관")
    category: Optional[str] = Field(None, description="카테고리")
    support_type: Optional[str] = Field(None, description="지원 유형")
    target_audience: Optional[str] = Field(None, description="지원 대상")
    budget: Optional[str] = Field(None, description="예산")
    application_start_date: Optional[date] = Field(None, description="신청 시작일")
    application_end_date: Optional[date] = Field(None, description="신청 종료일")
    description: Optional[str] = Field(None, description="상세 내용")
    contact_info: Optional[str] = Field(None, description="연락처")
    url: Optional[str] = Field(None, description="상세 URL")


class GovernmentSupportCreate(GovernmentSupportBase):
    """공고 생성 스키마"""
    source_api: str = Field(..., description="출처 API (MSIT/KSTARTUP)")


class GovernmentSupportResponse(GovernmentSupportBase):
    """공고 응답 스키마"""
    id: int
    source_api: str
    is_new: bool = Field(..., description="신규 공고 여부")
    first_crawled_at: Optional[datetime] = Field(None, description="최초 수집 시각")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FileInfo(BaseModel):
    """첨부파일 정보"""
    fileName: str
    fileUrl: str


class GovernmentSupportDetail(GovernmentSupportResponse):
    """공고 상세 스키마 (첨부파일 포함)"""
    files: Optional[List[FileInfo]] = Field(None, description="첨부파일 목록")


class GovernmentSupportListResponse(BaseModel):
    """공고 목록 응답"""
    total: int = Field(..., description="전체 개수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    items: List[GovernmentSupportResponse] = Field(..., description="공고 목록")


class StatsResponse(BaseModel):
    """통계 응답"""
    total_supports: int = Field(..., description="전체 공고 수")
    new_supports: int = Field(..., description="신규 공고 수")
    msit_supports: int = Field(..., description="과기부 공고 수")
    kstartup_supports: int = Field(..., description="K-Startup 공고 수")
    ongoing_supports: int = Field(..., description="진행 중 공고 수")
    upcoming_supports: int = Field(..., description="예정 공고 수")
    closed_supports: int = Field(..., description="마감 공고 수")
