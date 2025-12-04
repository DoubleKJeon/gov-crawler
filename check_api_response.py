"""
실제 API 응답 구조 확인
"""
import requests
import json
import os

MSIT_KEY = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
KSTARTUP_KEY = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

print("=" * 70)
print("실제 API 응답 구조 확인")
print("=" * 70)

# 1. MSIT API
print("\n[1/2] MSIT API 호출...")
try:
    url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
    params = {
        "serviceKey": MSIT_KEY,
        "numOfRows": 2,
        "pageNo": 1,
        "returnType": "json"
    }
    
    response = requests.get(url, params=params, timeout=30)
    print(f"상태 코드: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n전체 응답 구조:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        
        # 키 체크
        print("\n최상위 키:", list(data.keys()))
        if "response" in data:
            print("response 키:", list(data["response"].keys()))
            if "body" in data["response"]:
                body = data["response"]["body"]
                print("body 키:", list(body.keys()) if isinstance(body, dict) else type(body))
                if isinstance(body, dict) and "items" in body:
                    items = body["items"]
                    print("items 타입:", type(items))
                    print("items:", items)
    else:
        print(f"오류: {response.text[:500]}")
except Exception as e:
    print(f"실패: {e}")
    import traceback
    traceback.print_exc()

# 2. K-Startup API
print("\n" + "=" * 70)
print("[2/2] K-Startup API 호출...")
try:
    url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
    params = {
        "ServiceKey": KSTARTUP_KEY,
        "page": 1,
        "perPage": 2,
        "returnType": "json"
    }
    
    response = requests.get(url, params=params, timeout=30)
    print(f"상태 코드: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n전체 응답 구조:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        
        # 키 체크
        print("\n최상위 키:", list(data.keys()) if isinstance(data, dict) else type(data))
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
            print("items 타입:", type(items))
            print("items:", items)
    else:
        print(f"오류: {response.text[:500]}")
except Exception as e:
    print(f"실패: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
