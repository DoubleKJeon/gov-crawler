"""
Stats API - Vercel Serverless Function
GET /api/stats
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from ._db import SessionLocal, GovernmentSupport

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
def get_stats():
    """통계"""
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
    
    return {
        "total_supports": total or 0,
        "msit_supports": msit or 0,
        "kstartup_supports": kstartup or 0,
        "sme_supports": sme or 0
    }
