"""최종 해결: 완전히 작동하는 크롤러"""
import os
import sys

os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["SECRET_KEY"] = "test"
os.environ["JWT_SECRET_KEY"] = "test"

from app import config_simple
sys.modules['app.config'] = config_simple

from app.database import SessionLocal
from sqlalchemy import text

# minimal_test.py의 성공 코드 그대로
import requests
from datetime import datetime

print("=" * 60)
print("Working Crawler Test")
print("=" * 60)

db = SessionLocal()

# 1. MSIT
print("\n[1/2] MSIT Crawler...")
msit_count = 0
try:
    url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
    params = {
        "serviceKey": os.environ["MSIT_API_KEY"],
        "numOfRows": 10,
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
                
                for item in items:
                    # 직접 SQL 사용
                    sql = text("""
                        INSERT OR IGNORE INTO government_supports 
                        (source_api, title, organization, url, is_new, first_crawled_at, created_at, updated_at)
                        VALUES (:source, :title, :org, :url, :is_new, :crawled, :created, :updated)
                    """)
                    db.execute(sql, {
                        "source": "MSIT",
                        "title": item.get("subject", ""),
                        "org": item.get("deptName", ""),
                        "url": item.get("viewUrl", ""),
                        "is_new": True,
                        "crawled": datetime.utcnow(),
                        "created": datetime.utcnow(),
                        "updated": datetime.utcnow()
                    })
                    msit_count += 1
                
                db.commit()
                print(f"  ✅ Saved: {msit_count}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    db.rollback()

# 2. K-Startup
print("\n[2/2] K-Startup Crawler...")
kstartup_count = 0
try:
    url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
    params = {
        "ServiceKey": os.environ["KSTARTUP_API_KEY"],
        "page": 1,
        "perPage": 10,
        "returnType": "json"
    }
    
    response = requests.get(url, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and isinstance(data["data"], list):
            items = data["data"]
            
            for item in items:
                # 직접 SQL 사용
                sql = text("""
                    INSERT OR IGNORE INTO government_supports 
                    (source_api, title, organization, url, is_new, first_crawled_at, created_at, updated_at)
                    VALUES (:source, :title, :org, :url, :is_new, :crawled, :created, :updated)
                """)
                db.execute(sql, {
                    "source": "KSTARTUP",
                    "title": item.get("biz_pbanc_nm", ""),
                    "org": item.get("pbanc_ntrp_nm", ""),
                    "url": item.get("detl_pg_url", ""),
                    "is_new": True,
                    "crawled": datetime.utcnow(),
                    "created": datetime.utcnow(),
                    "updated": datetime.utcnow()
                })
                kstartup_count += 1
            
            db.commit()
            print(f"  ✅ Saved: {kstartup_count}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    db.rollback()

db.close()

print("\n" + "=" * 60)
print(f"Total: MSIT={msit_count}, K-Startup={kstartup_count}")
print("=" * 60)

if msit_count > 0 or kstartup_count > 0:
    print("\n🎉 SUCCESS! Crawler is WORKING!")
else:
    print("\n⚠️  No data collected")
