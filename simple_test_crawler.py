"""
간단한 크롤러 테스트
"""
import os
os.environ.setdefault("LOG_LEVEL", "INFO")

# API 키 직접 설정
MSIT_KEY = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
KSTARTUP_KEY = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

print("=" * 60)
print("크롤러 간단 테스트")
print("=" * 60)

# 1. 데이터베이스 초기화
print("\n[1] 데이터베이스 초기화...")
from app.database import Base, engine
Base.metadata.create_all(bind=engine)  
print("✓ 완료")

# 2. MSIT 크롤러 테스트
print("\n[2] 과기부 크롤러 테스트...")
from app.crawlers import MSITCrawler
from app.database import SessionLocal

msit = MSITCrawler(MSIT_KEY)
db = SessionLocal()

try:
    result = msit.run(db)
    print(f"결과: {result}")
except Exception as e:
    print(f"오류: {e}")
finally:
    db.close()

# 3. K-Startup 크롤러 테스트
print("\n[3] K-Startup 크롤러 테스트...")
from app.crawlers import KStartupCrawler

kstartup = KStartupCrawler(KSTARTUP_KEY)
db = SessionLocal()

try:
    result = kstartup.run(db)
    print(f"결과: {result}")
except Exception as e:
    print(f"오류: {e}")
finally:
    db.close()

# 4. 결과 확인
print("\n[4] 수집된 데이터 확인...")
from app.models import GovernmentSupport

db = SessionLocal()
try:
    total = db.query(GovernmentSupport).count()
    new = db.query(GovernmentSupport).filter(GovernmentSupport.is_new == True).count()
    msit_count = db.query(GovernmentSupport).filter(GovernmentSupport.source_api == "MSIT").count()
    kstartup_count = db.query(GovernmentSupport).filter(GovernmentSupport.source_api == "KSTARTUP").count()
    
    print(f"✓ 전체 공고: {total}개")
    print(f"✓ 신규 공고: {new}개")
    print(f"✓ 과기부: {msit_count}개")
    print(f"✓ K-Startup: {kstartup_count}개")
    
    if total > 0:
        print("\n[5] 샘플 데이터:")
        sample = db.query(GovernmentSupport).first()
        print(f"  제목: {sample.title}")
        print(f"  기관: {sample.organization}")
        print(f"  URL: {sample.url}")
        
finally:
    db.close()

print("\n" + "=" * 60)
print("테스트 완료")
print("=" * 60)
