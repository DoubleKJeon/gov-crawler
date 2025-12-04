"""
메인 DB에 데이터 수집 (init_db.py가 만든 gov_support.db 사용)
"""
import os
import sys

# 환경변수 설정
os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

# config_simple을 config로 대체
from app import config_simple
sys.modules['app.config'] = config_simple

from app.database import SessionLocal
from app.crawlers.msit import MSITCrawler
from app.crawlers.kstartup import KStartupCrawler

print("=" * 60)
print("메인 데이터베이스에 데이터 수집")
print("=" * 60)
print()

db = SessionLocal()

try:
    # MSIT 크롤러
    print("[1/2] 과기부 API 크롤링...")
    msit = MSITCrawler()
    msit_result = msit.run()
    print(f"  ✅ 수집: {msit_result['fetched']}개, 저장: {msit_result['saved']}개")
    
    # K-Startup 크롤러
    print("[2/2] K-Startup API 크롤링...")
    kstartup = KStartupCrawler()
    kstartup_result = kstartup.run()
    print(f"  ✅ 수집: {kstartup_result['fetched']}개, 저장: {kstartup_result['saved']}개")
    
    print()
    print("=" * 60)
    print(f"✅ 완료! 총 {msit_result['saved'] + kstartup_result['saved']}개 저장됨")
    print("=" * 60)
    
finally:
    db.close()
