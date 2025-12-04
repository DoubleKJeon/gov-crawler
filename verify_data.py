"""데이터 확인 스크립트"""
import requests

print("=" * 60)
print("데이터 확인")
print("=" * 60)
print()

# 1. 통계 확인
r = requests.get('http://localhost:8000/api/stats')
stats = r.json()
print(f"전체 공고: {stats.get('total_supports', 0)}개")
print(f"신규 공고: {stats.get('new_supports', 0)}개")
print()

# 2. 공고 목록 확인
r = requests.get('http://localhost:8000/api/supports?page=1&size=5')
data = r.json()
print(f"API 상태: {r.status_code}")
print(f"전체 공고: {data.get('total', 0)}개")
print(f"현재 페이지: {len(data.get('items', []))}개")
print()

if data.get('items'):
    print("공고 목록:")
    for i, item in enumerate(data['items'][:5], 1):
        title = item.get('title', 'N/A')
        source = item.get('source_api', 'N/A')
        print(f"  {i}. [{source}] {title[:50]}...")
else:
    print("❌ 공고가 없습니다!")
    print()
    print("크롤러를 다시 실행해보세요:")
    print("  POST http://localhost:8000/api/crawler/run")
