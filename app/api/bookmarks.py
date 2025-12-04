"""
북마크 API 라우터
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.support import GovernmentSupport
from app.schemas.bookmark import (
    BookmarkCreate,
    BookmarkUpdate,
    BookmarkResponse,
    # BookmarkWithSupport, # 임시 비활성화
)
from app.services.deps import get_current_user

router = APIRouter()


@router.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(
    bookmark_create: BookmarkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    북마크 추가
    
    인증 필요
    """
    # 공고 존재 확인
    support = db.query(GovernmentSupport).filter(
        GovernmentSupport.id == bookmark_create.support_id
    ).first()
    
    if not support:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 공고를 찾을 수 없습니다"
        )
    
    # 북마크 생성
    bookmark = Bookmark(
        user_id=current_user.id,
        support_id=bookmark_create.support_id,
        memo=bookmark_create.memo
    )
    
    try:
        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)
        return bookmark
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 북마크한 공고입니다"
        )


@router.get("/bookmarks", response_model=List[BookmarkResponse])
def get_my_bookmarks(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    내 북마크 목록
    
    인증 필요
    """
    skip = (page - 1) * size
    
    bookmarks = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id
    ).order_by(Bookmark.created_at.desc()).offset(skip).limit(size).all()
    
    return bookmarks


@router.get("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
def get_bookmark(
    bookmark_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    북마크 상세
    
    인증 필요
    """
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="북마크를 찾을 수 없습니다"
        )
    
    return bookmark


@router.put("/bookmarks/{bookmark_id}", response_model=BookmarkResponse)
def update_bookmark(
    bookmark_id: int,
    bookmark_update: BookmarkUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    북마크 수정 (메모만)
    
    인증 필요
    """
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="북마크를 찾을 수 없습니다"
        )
    
    if bookmark_update.memo is not None:
        bookmark.memo = bookmark_update.memo
    
    db.commit()
    db.refresh(bookmark)
    
    return bookmark


@router.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    bookmark_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    북마크 삭제
    
    인증 필요
    """
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="북마크를 찾을 수 없습니다"
        )
    
    db.delete(bookmark)
    db.commit()
    
    return None
