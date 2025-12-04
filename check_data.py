"""간단한 API 데이터 확인"""
import requests

print("API 데이터 확인 중...")
print()

try:
    r = requests.get('http://localhost:8000/api/supports?page=1&size=5')
    print(f"상태 코드: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"전체 공고 수: {data.get('total', 0)}")
        print(f"현재 페이지 항목: {len(data.get('items', []))}")
        
        if data.get('items'):
            print("\n첫 번째 공고:")
            item = data['items'][0]
            print(f"  제목: {item.get('title', 'N/A')}")
            print(f"  소스: {item.get('source_api', 'N/A')}")
        else:
            print("\n❌ 공고 데이터가 없습니다!")
            print("minimal_test.py를 다시 실행하세요.")
    else:
        print(f"❌ API 오류: {r.status_code}")
        
except Exception as e:
    print(f"❌ 오류: {e}")
