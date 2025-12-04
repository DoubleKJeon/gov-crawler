"""
Crawler API - Vercel Serverless Function
POST /api/crawler
"""
import os
import requests
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ._db import SessionLocal, GovernmentSupport

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def crawl_msit():
    """과기부 크롤링"""
    result = {"source": "MSIT", "success": False, "fetched": 0, "saved": 0}
    try:
        api_key = os.environ.get("MSIT_API_KEY")
        url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
        params = {
            "serviceKey": api_key,
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
                    session = SessionLocal()
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
    """K-Startup 크롤링"""
    result = {"source": "KSTARTUP", "success": False, "fetched": 0, "saved": 0}
    try:
        api_key = os.environ.get("KSTARTUP_API_KEY")
        url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
        params = {
            "ServiceKey": api_key,
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
                
                session = SessionLocal()
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

def crawl_sme():
    """기업마당 크롤링"""
    result = {"source": "SME", "success": False, "fetched": 0, "saved": 0}
    try:
        api_key = os.environ.get("KSTARTUP_API_KEY")
        url = "https://apis.data.go.kr/B553530/sme/getList"
        params = {
            "ServiceKey": api_key,
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
                    session = SessionLocal()
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

@app.post("/api/crawler")
def run_crawler():
    """크롤러 실행 (MSIT + K-Startup + SME)"""
    results = []
    results.append(crawl_msit())
    results.append(crawl_kstartup())
    results.append(crawl_sme())
    
    total_saved = sum(r.get("saved", 0) for r in results)
    return {
        "success": True,
        "message": f"크롤링 완료: {total_saved}개 저장",
        "results": results
    }
