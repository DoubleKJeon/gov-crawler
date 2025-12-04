"""
인증 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    LoginRequest,
    Token,
)
from app.services.auth import (
    authenticate_user,
    create_user,
    create_access_token,
    update_last_login,
    get_password_hash,
)
from app.services.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    회원가입
    
    - 이메일 중복 체크
    - 비밀번호 해싱
    - 사용자 생성
    """
    try:
        user = create_user(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    로그인
    
    - 이메일/비밀번호 검증
    - JWT 토큰 발급
    - 마지막 로그인 시간 업데이트
    """
    user = authenticate_user(db, login_request.email, login_request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 마지막 로그인 시간 업데이트
    update_last_login(db, user)
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    내 정보 조회
    
    인증 필요
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    내 정보 수정
    
    - 이름 변경
    - 비밀번호 변경
    
    인증 필요
    """
    # 이름 업데이트
    if user_update.name is not None:
        current_user.name = user_update.name
    
    # 비밀번호 업데이트
    if user_update.password is not None:
        current_user.password_hash = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    회원 탈퇴
    
    인증 필요
    """
    db.delete(current_user)
    db.commit()
    
    return None
