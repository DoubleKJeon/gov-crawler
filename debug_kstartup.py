"""API 응답 디버깅"""
import requests

KSTARTUP_KEY = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
params = {
    "ServiceKey": KSTARTUP_KEY,
    "page": 1,
    "perPage": 1,
    "returnType": "json"
}

response = requests.get(url, params=params, timeout=30)
print(f"상태: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("\n최상위 키:", list(data.keys()) if isinstance(data, dict) else type(data))
    
    if isinstance(data, dict):
        for key in data.keys():
            value = data[key]
            print(f"\n{key}: {type(value)}")
            if isinstance(value, dict):
                print(f"  하위 키: {list(value.keys())[:5]}")
            elif isinstance(value, list):
                print(f"  길이: {len(value)}")
                if value:
                    print(f"  첫 항목: {type(value[0])}")
else:
    print(f"오류: {response.text}")
