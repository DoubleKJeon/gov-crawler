"""
창업진흥원 K-Startup 크롤러
"""
from typing import List, Dict, Any
from datetime import datetime
import requests
from loguru import logger

from app.crawlers.base import BaseCrawler


class KStartupCrawler(BaseCrawler):
    """창업진흥원 K-Startup 크롤러"""
    
    BASE_URL = "https://apis.data.go.kr/B552735/kisedKstartupService01"
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "KSTARTUP")
        
        # 4가지 엔드포인트
        self.endpoints = {
            "announcements": f"{self.BASE_URL}/getAnnouncementInformation01",
            "business": f"{self.BASE_URL}/getBusinessInformation01",
            "contents": f"{self.BASE_URL}/getContentInformation01",
            "statistics": f"{self.BASE_URL}/getStatisticalInformation01",
        }
    
    def fetch_data(self, endpoint_type: str = "announcements", page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        K-Startup API에서 데이터를 가져옵니다.
        
        Args:
            endpoint_type: API 유형 (announcements, business, contents, statistics)
            page: 페이지 번호
            per_page: 한 페이지 결과 수
            
        Returns:
            원본 데이터 리스트
        """
        endpoint = self.endpoints.get(endpoint_type, self.endpoints["announcements"])
        
        try:
            params = {
                "ServiceKey": self.api_key,  # 대소문자 주의!
                "page": page,
                "perPage": per_page,
                "returnType": "json"
            }
            
            logger.debug(f"🔗 요청 URL: {endpoint}")
            
            response = requests.get(
                endpoint,
                params=params,
                timeout=30
            )
            
            logger.info(f"📨 응답 상태: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            
            # 응답 구조: items > item
            if isinstance(data, dict) and "items" in data:
                items = data["items"]
                if isinstance(items, dict) and "item" in items:
                    result = items["item"]
                    # item이 dict면 list로 변환
                    if isinstance(result, dict):
                        return [result]
                    return result if isinstance(result, list) else []
                elif isinstance(items, list):
                    return items
            
            return []
            
        except requests.RequestException as e:
            logger.error(f"❌ API 호출 실패: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"응답 내용: {e.response.text[:500]}")
            return []
    
    def parse_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        K-Startup 데이터를 통합 형식으로 파싱합니다.
        
        API 필드 (snake_case):
        - biz_pbanc_nm: 지원사업 공고명
        - pbanc_rcpt_bgng_dt: 공고 접수 시작 일시
        - pbanc_rcpt_end_dt: 공고 접수 종료 일시
        - supt_biz_clsfc: 지원 분야
        - aply_trgt: 신청 대상
        - pbanc_ntrp_nm: 창업 지원 기관명
        - sprv_inst: 주관 기관
        - detl_pg_url: 상세페이지 URL
        """
        return {
            "title": item.get("biz_pbanc_nm", ""),
            "organization": item.get("pbanc_ntrp_nm") or item.get("sprv_inst", "창업진흥원"),
            "category": item.get("supt_biz_clsfc", "창업지원"),
            "support_type": item.get("supt_biz_chrct"),
            "target_audience": item.get("aply_trgt_ctnt") or item.get("aply_trgt"),
            "budget": item.get("biz_supt_bdgt_info"),
            "application_start_date": self._parse_date(item.get("pbanc_rcpt_bgng_dt")),
            "application_end_date": self._parse_date(item.get("pbanc_rcpt_end_dt")),
            "description": item.get("pbanc_ctnt") or item.get("biz_supt_ctnt"),
            "contact_info": item.get("prch_cnpl_no") or item.get("biz_prch_dprt_nm"),
            "url": item.get("detl_pg_url", ""),
            "files": None,  # K-Startup API는 파일 정보 없음
        }
    
    def _parse_date(self, date_str: Any) -> Any:
        """날짜 문자열을 date 객체로 변환"""
        if not date_str:
            return None
        
        try:
            # "2012-11-29 00:00:00" 또는 "20121129" 형식
            if isinstance(date_str, str):
                # 공백 포함된 경우
                if " " in date_str:
                    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                # 하이픈 포함
                elif "-" in date_str:
                    return datetime.strptime(date_str, "%Y-%m-%d").date()
                # 숫자만 있는 경우
                elif len(date_str) == 8:
                    return datetime.strptime(date_str, "%Y%m%d").date()
            return date_str
        except Exception as e:
            logger.warning(f"⚠️ 날짜 파싱 실패: {date_str} - {e}")
            return None
