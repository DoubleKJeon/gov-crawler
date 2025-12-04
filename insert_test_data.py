"""
테스트 데이터 삽입
"""
import os
import sys

os.environ["SECRET_KEY"] = "test"
os.environ["JWT_SECRET_KEY"] = "test"

from app import config_simple
sys.modules['app.config'] = config_simple

from app.database import SessionLocal
from app.models.support import GovernmentSupport
from datetime import datetime, date, timedelta

print("테스트 데이터 삽입 중...")

db = SessionLocal()

try:
    # 테스트 공고 5개
    test_data = [
        {
            "title": "AI 스타트업 육성 지원사업",
            "organization": "과학기술정보통신부",
            "category": "창업지원",
            "source": "MSIT",
            "deadline": date.today() + timedelta(days=15)
        },
        {
            "title": "중소기업 R&D 과제 지원",
            "organization": "중소벤처기업부",
            "category": "R&D",
            "source": "KSTARTUP",
            "deadline": date.today() + timedelta(days=7)
        },
        {
            "title": "스타트업 글로벌 진출 지원",
            "organization": "K-Startup",
            "category": "해외진출",
            "source": "KSTARTUP",
            "deadline": date.today() + timedelta(days=30)
        },
        {
            "title": "벤처기업 인증 지원사업",
            "organization": "중소벤처기업부",
            "category": "인증지원",
            "source": "KSTARTUP",
            "deadline": date.today() + timedelta(days=3)
        },
        {
            "title": "데이터 바우처 지원사업",
            "organization": "한국데이터산업진흥원",
            "category": "데이터",
            "source": "MSIT",
            "deadline": date.today() + timedelta(days=20)
        },
    ]
    
    for item in test_data:
        support = GovernmentSupport(
            source_api=item["source"],
            title=item["title"],
            organization=item["organization"],
            category=item["category"],
            support_type="지원사업",
            target_audience="중소기업, 스타트업",
            application_start_date=date.today() - timedelta(days=5),
            application_end_date=item["deadline"],
            description=f"{item['title']}에 대한 상세 설명입니다. 자격 요건을 확인하시고 신청하세요.",
            budget="최대 5천만원 ~ 5억원",
            url="https://www.k-startup.go.kr",
            is_new=True,
            first_crawled_at=datetime.now()
        )
        db.add(support)
    
    db.commit()
    print(f"✅ {len(test_data)}개 테스트 공고 저장 완료!")
    
except Exception as e:
    print(f"❌ 오류: {e}")
    db.rollback()
finally:
    db.close()
