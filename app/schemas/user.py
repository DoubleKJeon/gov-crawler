"""
사용자 인증 스키마
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr = Field(..., description="이메일")
    name: Optional[str] = Field(None, description="이름")


class UserCreate(UserBase):
    """사용자 생성 스키마"""
    password: str = Field(..., min_length=6, description="비밀번호 (최소 6자)")


class UserUpdate(BaseModel):
    """사용자 수정 스키마"""
    name: Optional[str] = Field(None, description="이름")
    password: Optional[str] = Field(None, min_length=6, description="새 비밀번호")


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """토큰 응답"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰 데이터"""
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str
