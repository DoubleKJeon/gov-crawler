"""
작동하는 크롤러 (minimal_test.py 기반)
"""
import os
import requests
from datetime import datetime
from app.database import SessionLocal
from app.models import GovernmentSupport

def crawl_msit():
    """과기부 API 크롤링 (minimal_test.py 검증된 코드)"""
    result = {"source": "MSIT", "success": False, "fetched": 0, "saved": 0}
    db = SessionLocal()
    
    try:
        api_key = os.environ.get("MSIT_API_KEY")
        url = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
        params = {
            "serviceKey": api_key,
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
                    
                    result["fetched"] = len(items)
                    
                    for item in items:
                        support = GovernmentSupport(
                            source_api="MSIT",
                            title=item.get("subject", ""),
                            organization=item.get("deptName", ""),
                            url=item.get("viewUrl", "")
                        )
                        db.add(support)
                        result["saved"] += 1
                    
                    db.commit()
                    result["success"] = True
                else:
                    result["message"] = f"No items in response"
            else:
                result["message"] = f"No response key"
        else:
            result["message"] = f"HTTP {response.status_code}"
            
    except Exception as e:
        result["message"] = str(e)
        db.rollback()
    finally:
        db.close()
    
    return result


def crawl_kstartup():
    """K-Startup API 크롤링 (실제 응답 구조 반영)"""
    result = {"source": "KSTARTUP", "success": False, "fetched": 0, "saved": 0}
    db = SessionLocal()
    
    try:
        api_key = os.environ.get("KSTARTUP_API_KEY")
        url = "https://apis.data.go.kr/B552735/kisedKstartupService01/getAnnouncementInformation01"
        params = {
            "ServiceKey": api_key,
            "page": 1,
            "perPage": 10,
            "returnType": "json"
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # 실제 응답: data 키에 리스트
            if "data" in data and isinstance(data["data"], list):
                items = data["data"]
                result["fetched"] = len(items)
                
                for item in items:
                    support = GovernmentSupport(
                        source_api="KSTARTUP",
                        title=item.get("biz_pbanc_nm", ""),
                        organization=item.get("pbanc_ntrp_nm", ""),
                        url=item.get("detl_pg_url", "")
                    )
                    db.add(support)
                    result["saved"] += 1
                
                db.commit()
                result["success"] = True
            else:
                result["message"] = f"No data key or not list"
        else:
            result["message"] = f"HTTP {response.status_code}"
            
    except Exception as e:
        result["message"] = str(e)
        db.rollback()
    finally:
        db.close()
    
    return result


def run_all_crawlers():
    """모든 크롤러 실행"""
    print("=" * 60)
    print("크롤러 실행")
    print("=" * 60)
    
    results = []
    
    # MSIT
    print("\n[1/2] MSIT 크롤링...")
    msit_result = crawl_msit()
    results.append(msit_result)
    if msit_result["success"]:
        print(f"  ✅ 성공: {msit_result['saved']}개 저장")
    else:
        print(f"  ❌ 실패: {msit_result.get('message', 'Unknown error')}")
    
    # K-Startup
    print("\n[2/2] K-Startup 크롤링...")
    kstartup_result = crawl_kstartup()
    results.append(kstartup_result)
    if kstartup_result["success"]:
        print(f"  ✅ 성공: {kstartup_result['saved']}개 저장")
    else:
        print(f"  ❌ 실패: {kstartup_result.get('message', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    total_saved = sum(r.get("saved", 0) for r in results)
    print(f"총 {total_saved}개 저장")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    run_all_crawlers()
