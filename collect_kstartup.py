"""
K-Startup만 수집 (MSIT는 에러 있음)
"""
import os
import sys

os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["SECRET_KEY"] = "test"
os.environ["JWT_SECRET_KEY"] = "test"

from app import config_simple
sys.modules['app.config'] = config_simple

from app.database import SessionLocal
from app.models.support import GovernmentSupport
from datetime import datetime, date

print("K-Startup 데이터 수집 중...")

db = SessionLocal()

try:
    import requests
    url = "https://apis.data.go.kr/B552735/k-startupInfo/getBusinessList"
    params = {
        "serviceKey": os.environ["KSTARTUP_API_KEY"],
        "numOfRows": "10",
        "pageNo": "1",
        "type": "json"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        
        saved = 0
        for item in items:
            support = GovernmentSupport(
                source_api="KSTARTUP",
                title=item.get('bizAnnTitle', '제목없음'),
                organization=item.get('bsnDept', 'K-Startup'),
                category=item.get('bizAnnCategory', '지원사업'),
                support_type="지원사업",
                target_audience=item.get('targetDescript', '중소기업, 스타트업'),
                application_start_date=date.today(),
                application_end_date=date.today(),
                description=item.get('bizAnnTitle', ''),
                url=item.get('bizAnnUrl', ''),
                is_new=True,
                first_crawled_at=datetime.now()
            )
            db.add(support)
            saved += 1
        
        db.commit()
        print(f"✅ {saved}개 저장 완료!")
    else:
        print(f"❌ API 오류: {response.status_code}")
except Exception as e:
    print(f"❌ 오류: {e}")
    db.rollback()
finally:
    db.close()
