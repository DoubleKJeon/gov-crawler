"""
정부지원사업 API 라우터
"""
from typing import Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_

from app.database import get_db
from app.models.support import GovernmentSupport
from app.schemas.support import (
    GovernmentSupportResponse,
    GovernmentSupportDetail,
    GovernmentSupportListResponse,
    StatsResponse,
)

router = APIRouter()


@router.get("/supports", response_model=GovernmentSupportListResponse)
def get_supports(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    source: Optional[str] = Query(None, description="출처 (MSIT/KSTARTUP)"),
    category: Optional[str] = Query(None, description="카테고리"),
    is_new: Optional[bool] = Query(None, description="신규 공고만"),
    db: Session = Depends(get_db)
):
    """
    공고 목록 조회 (페이지네이션)
    """
    query = db.query(GovernmentSupport)
    
    # 필터링
    if source:
        query = query.filter(GovernmentSupport.source_api == source.upper())
    if category:
        query = query.filter(GovernmentSupport.category == category)
    if is_new is not None:
        query = query.filter(GovernmentSupport.is_new == is_new)
    
    # 전체 개수
    total = query.count()
    
    # 페이지네이션
    skip = (page - 1) * size
    items = query.order_by(GovernmentSupport.created_at.desc()).offset(skip).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": items
    }


@router.get("/supports/new", response_model=GovernmentSupportListResponse)
def get_new_supports(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
):
    """
    신규 공고만 조회
    """
    query = db.query(GovernmentSupport).filter(GovernmentSupport.is_new == True)
    
    total = query.count()
    skip = (page - 1) * size
    items = query.order_by(GovernmentSupport.first_crawled_at.desc()).offset(skip).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": items
    }


@router.get("/supports/search", response_model=GovernmentSupportListResponse)
def search_supports(
    keyword: Optional[str] = Query(None, description="검색 키워드"),
    category: Optional[str] = Query(None, description="카테고리"),
    organization: Optional[str] = Query(None, description="기관명"),
    status: Optional[str] = Query(None, description="진행 상태 (ongoing/upcoming/closed)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
):
    """
    공고 검색
    
    - keyword: 제목, 내용에서 검색
    - category: 카테고리 필터
    - organization: 기관명 필터
    - status: 진행 상태 필터
      - ongoing: 진행 중 (접수 기간 내)
      - upcoming: 예정 (접수 시작 전)
      - closed: 마감 (접수 종료)
    """
    query = db.query(GovernmentSupport)
    
    # 키워드 검색 (제목 + 내용)
    if keyword:
        search_filter = or_(
            GovernmentSupport.title.ilike(f"%{keyword}%"),
            GovernmentSupport.description.ilike(f"%{keyword}%")
        )
        query = query.filter(search_filter)
    
    # 카테고리 필터
    if category:
        query = query.filter(GovernmentSupport.category == category)
    
    # 기관명 필터
    if organization:
        query = query.filter(GovernmentSupport.organization.ilike(f"%{organization}%"))
    
    # 진행 상태 필터
    if status:
        today = date.today()
        
        if status == "ongoing":
            # 진행 중: 시작일 <= 오늘 <= 종료일
            query = query.filter(
                and_(
                    GovernmentSupport.application_start_date <= today,
                    GovernmentSupport.application_end_date >= today
                )
            )
        elif status == "upcoming":
            # 예정: 시작일 > 오늘
            query = query.filter(GovernmentSupport.application_start_date > today)
        elif status == "closed":
            # 마감: 종료일 < 오늘
            query = query.filter(GovernmentSupport.application_end_date < today)
    
    # 전체 개수
    total = query.count()
    
    # 페이지네이션
    skip = (page - 1) * size
    items = query.order_by(GovernmentSupport.created_at.desc()).offset(skip).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": items
    }


@router.get("/supports/{support_id}", response_model=GovernmentSupportDetail)
def get_support_detail(
    support_id: int,
    db: Session = Depends(get_db)
):
    """
    공고 상세 조회
    """
    support = db.query(GovernmentSupport).filter(GovernmentSupport.id == support_id).first()
    
    if not support:
        raise HTTPException(status_code=404, detail="해당 공고를 찾을 수 없습니다")
    
    return support


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    전체 통계
    """
    today = date.today()
    
    # 전체 공고 수
    total_supports = db.query(func.count(GovernmentSupport.id)).scalar()
    
    # 신규 공고 수
    new_supports = db.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.is_new == True
    ).scalar()
    
    # 출처별 공고 수
    msit_supports = db.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.source_api == "MSIT"
    ).scalar()
    
    kstartup_supports = db.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.source_api == "KSTARTUP"
    ).scalar()
    
    # 진행 중 공고 (시작일 <= 오늘 <= 종료일)
    ongoing_supports = db.query(func.count(GovernmentSupport.id)).filter(
        and_(
            GovernmentSupport.application_start_date <= today,
            GovernmentSupport.application_end_date >= today
        )
    ).scalar()
    
    # 예정 공고 (시작일 > 오늘)
    upcoming_supports = db.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.application_start_date > today
    ).scalar()
    
    # 마감 공고 (종료일 < 오늘)
    closed_supports = db.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.application_end_date < today
    ).scalar()
    
    return {
        "total_supports": total_supports or 0,
        "new_supports": new_supports or 0,
        "msit_supports": msit_supports or 0,
        "kstartup_supports": kstartup_supports or 0,
        "ongoing_supports": ongoing_supports or 0,
        "upcoming_supports": upcoming_supports or 0,
    "closed_supports": closed_supports or 0,
    }


@router.post("/crawler/run")
def run_crawler_manual(db: Session = Depends(get_db)):
    """
    수동 크롤링 실행
    
    minimal_test.py 기반 - 필수 필드만 사용
    """
    import os
    import requests
    from datetime import datetime
    
    results = []
    
    # 1. 과기부 API
    msit_result = {"source": "MSIT", "success": False}
    try:
        api_key = os.environ.get("MSIT_API_KEY", "")
        url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
        params = {
            "serviceKey": api_key,
            "numOfRows": 10,
            "pageNo": 1,
            "returnType": "json"
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                body = data["response"].get("body", {})
                items_wrapper = body.get("items", {})
                if "item" in items_wrapper:
                    items = items_wrapper["item"]
                    if isinstance(items, dict):
                        items = [items]
                    
                    saved = 0
                    for item in items:
                        # 필수 필드만 사용
                        support = GovernmentSupport(
                            source_api="MSIT",
                            title=item.get("subject", ""),
                            organization=item.get("deptName", ""),
                            url=item.get("viewUrl", ""),
                            is_new=True,
                            first_crawled_at=datetime.utcnow()
                        )
                        db.add(support)
                        saved += 1
                    
                    db.commit()
                    msit_result["success"] = True
                    msit_result["fetched"] = len(items)
                    msit_result["saved"] = saved
                else:
                    msit_result["message"] = f"items_wrapper keys: {list(items_wrapper.keys()) if isinstance(items_wrapper, dict) else type(items_wrapper)}"
            else:
                msit_result["message"] = f"response key missing. Keys: {list(data.keys())}"
        else:
            msit_result["message"] = f"HTTP {response.status_code}"
    except Exception as e:
        msit_result["message"] = str(e)
        db.rollback()
    
    results.append(msit_result)
    
    # 2. K-Startup API
    kstartup_result = {"source": "KSTARTUP", "success": False}
    try:
        api_key = os.environ.get("KSTARTUP_API_KEY", "")
        url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
        params = {
            "ServiceKey": api_key,
            "page": 1,
            "perPage": 10,
            "returnType": "json"
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # 실제: data 키에 리스트
            if "data" in data and isinstance(data["data"], list):
                items = data["data"]
                
                saved = 0
                for item in items:
                    # 필수 필드만 사용
                    support = GovernmentSupport(
                        source_api="KSTARTUP",
                        title=item.get("biz_pbanc_nm", ""),
                        organization=item.get("pbanc_ntrp_nm", ""),
                        url=item.get("detl_pg_url", ""),
                        is_new=True,
                        first_crawled_at=datetime.utcnow()
                    )
                    db.add(support)
                    saved += 1
                
                db.commit()
                kstartup_result["success"] = True
                kstartup_result["fetched"] = len(items)
                kstartup_result["saved"] = saved
            else:
                kstartup_result["message"] = f"data key missing or not list. Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
        else:
            kstartup_result["message"] = f"HTTP {response.status_code}"
    except Exception as e:
        kstartup_result["message"] = str(e)
        db.rollback()
    
    results.append(kstartup_result)
    
    return {
        "success": True,
        "message": "크롤링 완료",
        "results": results
    }
