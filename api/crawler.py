"""
Crawler API - Vercel Serverless Handler
POST /api/crawler
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# DB 설정
DATABASE_URL = os.environ.get("DATABASE_URL", "")
Base = declarative_base()

class GovernmentSupport(Base):
    __tablename__ = "government_supports"
    id = Column(Integer, primary_key=True)
    source_api = Column(String(20))
    title = Column(String(500))
    organization = Column(String(200))
    url = Column(String(1000), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
else:
    engine = create_engine("sqlite:///./gov_support.db")
    SessionLocal = sessionmaker(bind=engine)

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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # K-Startup만 크롤링 (가장 안정적)
            results = [crawl_kstartup()]
            
            total_saved = sum(r.get("saved", 0) for r in results)
            response_data = {
                "success": True,
                "message": f"크롤링 완료: {total_saved}개 저장",
                "results": results
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
