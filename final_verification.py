"""최종 확인 테스트"""
import requests
import json
import time

print("서버 시작 대기...")
time.sleep(3)

print("\n크롤러 API 호출 중...")
try:
    response = requests.post("http://localhost:8000/api/crawler/run", timeout=120)
    print(f"상태 코드: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        print("=" * 70)
        print("크롤링 결과:")
        print("=" * 70)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 70)
        
        # 각 크롤러 결과 확인
        for r in result.get("results", []):
            source = r.get("source")
            success = r.get("success")
            
            if success:
                print(f"\n✅ {source}: 성공")
                print(f"   수집: {r.get('fetched')}개")
                print(f"   저장: {r.get('saved')}개")
            else:
                print(f"\n❌ {source}: 실패")
                print(f"   메시지: {r.get('message')}")
        
        # 최종 판정
        all_success = all(r.get("success", False) for r in result.get("results", []))
        print("\n" + "=" * 70)
        if all_success:
            print("🎉 모든 크롤러 성공!")
        else:
            print("⚠️  일부 크롤러 실패")
        print("=" * 70)
    else:
        print(f"HTTP 오류: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"테스트 실패: {e}")
    import traceback
    traceback.print_exc()
