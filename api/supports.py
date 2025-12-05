"""
Supports API - Vercel Serverless Handler
GET /api/supports
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        page = int(params.get('page', ['1'])[0])
        size = int(params.get('size', ['20'])[0])
        
        try:
            session = SessionLocal()
            query = session.query(GovernmentSupport)
            total = query.count()
            skip = (page - 1) * size
            items = query.order_by(GovernmentSupport.created_at.desc()).offset(skip).limit(size).all()
            session.close()
            
            result = {
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
