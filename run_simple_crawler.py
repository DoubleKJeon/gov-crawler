"""
단순하고 작동하는 크롤러 (minimal_test.py 100% 기반)
Import 문제 없이 독립 실행
"""
import os
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 환경변수
os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

# DB 설정
Base = declarative_base()

class GovernmentSupport(Base):
    __tablename__ = "government_supports"
    id = Column(Integer, primary_key=True)
    source_api = Column(String(20))
    title = Column(String(500))
    organization = Column(String(200))
    url = Column(String(1000), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# DB 엔진
engine = create_engine("sqlite:///./gov_support.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

print("=" * 70)
print("정부지원사업 크롤러 - 간단 버전")
print("=" * 70)

results = []

# 1. 과기부
print("\n[1/2] MSIT 크롤링...")
msit_result = {"source": "MSIT", "success": False, "fetched": 0, "saved": 0}
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
                
                msit_result["fetched"] = len(items)
                session = Session()
                for item in items:
                    support = GovernmentSupport(
                        source_api="MSIT",
                        title=item.get("subject", ""),
                        organization=item.get("deptName", ""),
                        url=item.get("viewUrl", "")
                    )
                    session.add(support)
                    msit_result["saved"] += 1
                session.commit()
                session.close()
                msit_result["success"] = True
                print(f"  ✅ 성공: {msit_result['saved']}개 저장")
except Exception as e:
    msit_result["message"] = str(e)
    print(f"  ❌ 실패: {e}")

results.append(msit_result)

# 2. K-Startup
print("\n[2/2] K-Startup 크롤링...")
kstartup_result = {"source": "KSTARTUP", "success": False, "fetched": 0, "saved": 0}
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
            kstartup_result["fetched"] = len(items)
            
            session = Session()
            for item in items:
                support = GovernmentSupport(
                    source_api="KSTARTUP",
                    title=item.get("biz_pbanc_nm", ""),
                    organization=item.get("pbanc_ntrp_nm", ""),
                    url=item.get("detl_pg_url", "")
                )
                session.add(support)
                kstartup_result["saved"] += 1
            session.commit()
            session.close()
            kstartup_result["success"] = True
            print(f"  ✅ 성공: {kstartup_result['saved']}개 저장")
except Exception as e:
    kstartup_result["message"] = str(e)
    print(f"  ❌ 실패: {e}")

results.append(kstartup_result)

# 결과
print("\n" + "=" * 70)
total_saved = sum(r.get("saved", 0) for r in results)
total_success = sum(1 for r in results if r.get("success"))
print(f"결과: {total_success}/2 성공, 총 {total_saved}개 저장")
print("=" * 70)

if total_saved > 0:
    print("\n✅ 크롤러가 정상 작동합니다!")
else:
    print("\n⚠️  데이터 수집 실패")
