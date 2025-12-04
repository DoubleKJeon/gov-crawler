"""DB 직접 확인"""
import os
import sys

os.environ["SECRET_KEY"] = "test"
os.environ["JWT_SECRET_KEY"] = "test"

from app import config_simple
sys.modules['app.config'] = config_simple

from app.database import SessionLocal
from app.models.support import GovernmentSupport

db = SessionLocal()

print("=" * 60)
print("데이터베이스 직접 확인")
print("=" * 60)

total = db.query(GovernmentSupport).count()
msit = db.query(GovernmentSupport).filter(GovernmentSupport.source_api == "MSIT").count()
kstartup = db.query(GovernmentSupport).filter(GovernmentSupport.source_api == "KSTARTUP").count()

print(f"\n전체 공고: {total}개")
print(f"과기부: {msit}개")
print(f"K-Startup: {kstartup}개")

if total > 0:
    print("\n공고 목록:")
    supports = db.query(GovernmentSupport).limit(5).all()
    for i, s in enumerate(supports, 1):
        print(f"  {i}. [{s.source_api}] {s.title[:60]}...")
        print(f"     기관: {s.organization}")
    print(f"\n✅ 크롤러가 정상 작동했습니다!")
else:
    print("\n❌ 데이터가 없습니다.")

db.close()
