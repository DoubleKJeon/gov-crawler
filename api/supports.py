"""
Supports API - Vercel Serverless Function
GET /api/supports
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ._db import SessionLocal, GovernmentSupport

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/supports")
def get_supports(page: int = 1, size: int = 20):
    """공고 목록 조회"""
    session = SessionLocal()
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
