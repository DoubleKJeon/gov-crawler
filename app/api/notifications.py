"""
알림 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.notification import NotificationSetting
from app.schemas.notification import (
    NotificationSettingResponse,
    NotificationSettingUpdate,
)
from app.services.deps import get_current_user

router = APIRouter()


@router.get("/notifications/settings", response_model=NotificationSettingResponse)
def get_notification_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    내 알림 설정 조회
    
    인증 필요
    """
    setting = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == current_user.id
    ).first()
    
    # 설정이 없으면 기본값으로 생성
    if not setting:
        setting = NotificationSetting(user_id=current_user.id)
        db.add(setting)
        db.commit()
        db.refresh(setting)
    
    return setting


@router.put("/notifications/settings", response_model=NotificationSettingResponse)
def update_notification_settings(
    setting_update: NotificationSettingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    알림 설정 변경
    
    인증 필요
    """
    setting = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == current_user.id
    ).first()
    
    # 설정이 없으면 생성
    if not setting:
        setting = NotificationSetting(
            user_id=current_user.id,
            **setting_update.model_dump()
        )
        db.add(setting)
    else:
        # 기존 설정 업데이트
        for key, value in setting_update.model_dump().items():
            setattr(setting, key, value)
    
    db.commit()
    db.refresh(setting)
    
    return setting
