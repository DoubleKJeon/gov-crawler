"""크롤러 실행"""
import requests

print("크롤러 실행 중...")

try:
    # 크롤러 실행
    r = requests.post("https://gov-crawler-7.vercel.app/api/crawler", timeout=120)
    
    if r.status_code == 200:
        result = r.json()
        print(f"✅ {result.get('message')}")
        
        for source in result.get('results', []):
            status = "✅" if source.get('success') else "❌"
            print(f"{status} {source.get('source')}: {source.get('saved', 0)}개 저장")
    else:
        print(f"❌ 오류: {r.status_code}")
        print(r.text)
    
    # 통계
    r = requests.get("https://gov-crawler-7.vercel.app/api/stats")
    stats = r.json()
    print(f"\n총 {stats.get('total_supports', 0)}개 공고")
    
except Exception as e:
    print(f"❌ {e}")
