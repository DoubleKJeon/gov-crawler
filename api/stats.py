"""
Stats API - Vercel Serverless Handler
GET /api/stats
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            session = SessionLocal()
            total = session.query(func.count(GovernmentSupport.id)).scalar()
            msit = session.query(func.count(GovernmentSupport.id)).filter(
                GovernmentSupport.source_api == "MSIT"
            ).scalar()
            kstartup = session.query(func.count(GovernmentSupport.id)).filter(
                GovernmentSupport.source_api == "KSTARTUP"
            ).scalar()
            sme = session.query(func.count(GovernmentSupport.id)).filter(
                GovernmentSupport.source_api == "SME"
            ).scalar()
            session.close()
            
            result = {
                "total_supports": total or 0,
                "msit_supports": msit or 0,
                "kstartup_supports": kstartup or 0,
                "sme_supports": sme or 0
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
