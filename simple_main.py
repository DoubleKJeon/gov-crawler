"""
간단한 FastAPI 앱
run_simple_crawler.py의 크롤러 함수를 API로 노출
"""
import os
os.environ.setdefault("MSIT_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")
os.environ.setdefault("KSTARTUP_API_KEY", "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg==")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="정부지원사업 크롤러 API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 설정
Base = declarative_base()

class GovernmentSupport(Base):
    __tablename__ = "government_supports"
    id = Column(Integer, primary_key=True)
    source_api = Column(String(20))
    title = Column(String(500))
    organization = Column(String(200))
    url = Column(String(1000), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine("sqlite:///./gov_support.db")
Session = sessionmaker(bind=engine)


# 크롤러 함수 (run_simple_crawler.py와 동일)
def crawl_msit():
    result = {"source": "MSIT", "success": False, "fetched": 0, "saved": 0}
    try:
        url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
        params = {
            "serviceKey": os.environ.get("MSIT_API_KEY"),
            "numOfRows": 100,
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
                    
                    result["fetched"] = len(items)
                    session = Session()
                    for item in items:
                        support = GovernmentSupport(
                            source_api="MSIT",
                            title=item.get("subject", ""),
                            organization=item.get("deptName", ""),
                            url=item.get("viewUrl", "")
                        )
                        session.add(support)
                        result["saved"] += 1
                    session.commit()
                    session.close()
                    result["success"] = True
    except Exception as e:
        result["message"] = str(e)
    return result


def crawl_kstartup():
    result = {"source": "KSTARTUP", "success": False, "fetched": 0, "saved": 0}
    try:
        url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
        params = {
            "ServiceKey": os.environ.get("KSTARTUP_API_KEY"),
            "page": 1,
            "perPage": 100,
            "returnType": "json"
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and isinstance(data["data"], list):
                items = data["data"]
                result["fetched"] = len(items)
                
                session = Session()
                for item in items:
                    support = GovernmentSupport(
                        source_api="KSTARTUP",
                        title=item.get("biz_pbanc_nm", ""),
                        organization=item.get("pbanc_ntrp_nm", ""),
                        url=item.get("detl_pg_url", "")
                    )
                    session.add(support)
                    result["saved"] += 1
                session.commit()
                session.close()
                result["success"] = True
    except Exception as e:
        result["message"] = str(e)
    return result


# API 엔드포인트
@app.get("/")
def read_root():
    return {"message": "정부지원사업 크롤러 API", "docs": "/docs"}


def crawl_sme():
    """기업마당 (SME) API 크롤링"""
    result = {"source": "SME", "success": False, "fetched": 0, "saved": 0}
    try:
        # 기업마당 API (공공데이터포털)
        url = "https://apis.data.go.kr/B553530/sme/getList"
        params = {
            "ServiceKey": os.environ.get("KSTARTUP_API_KEY"),  # 같은 키 사용
            "numOfRows": 100,
            "pageNo": 1,
            "type": "json"
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
                    
                    result["fetched"] = len(items)
                    session = Session()
                    for item in items:
                        support = GovernmentSupport(
                            source_api="SME",
                            title=item.get("title", ""),
                            organization=item.get("orgName", ""),
                            url=item.get("url", "")
                        )
                        session.add(support)
                        result["saved"] += 1
                    session.commit()
                    session.close()
                    result["success"] = True
    except Exception as e:
        result["message"] = str(e)
    return result


@ app.post("/api/crawler/run")
def run_crawler():
    """크롤러 실행 (MSIT + K-Startup + SME)"""
    results = []
    results.append(crawl_msit())
    results.append(crawl_kstartup())
    results.append(crawl_sme())
    
    total_saved = sum(r.get("saved", 0) for r in results)
    return {
        "success": True,
        "message": f"크롤링 완료: {total_saved}개 저장 (MSIT + K-Startup + SME)",
        "results": results
    }


@app.get("/api/supports")
def get_supports(page: int = 1, size: int = 20):
    """공고 목록 조회"""
    session = Session()
    query = session.query(GovernmentSupport)
    total = query.count()
    skip = (page - 1) * size
    items = query.order_by(GovernmentSupport.created_at.desc()).offset(skip).limit(size).all()
    session.close()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [
            {
                "id": item.id,
                "source_api": item.source_api,
                "title": item.title,
                "organization": item.organization,
                "url": item.url,
                "created_at": item.created_at.isoformat()
            }
            for item in items
        ]
    }


@app.get("/api/stats")
def get_stats():
    """통계"""
    session = Session()
    total = session.query(func.count(GovernmentSupport.id)).scalar()
    msit = session.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.source_api == "MSIT"
    ).scalar()
    kstartup = session.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.source_api == "KSTARTUP"
    ).scalar()
    session.close()
    
    sme = session.query(func.count(GovernmentSupport.id)).filter(
        GovernmentSupport.source_api == "SME"
    ).scalar()
    session.close()
    
    return {
        "total_supports": total or 0,
        "msit_supports": msit or 0,
        "kstartup_supports": kstartup or 0,
        "sme_supports": sme or 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
