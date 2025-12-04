"""
과학기술정보통신부 사업공고 크롤러
"""
from typing import List, Dict, Any
from datetime import datetime
import requests
from loguru import logger

from app.crawlers.base import BaseCrawler


class MSITCrawler(BaseCrawler):
    """과학기술정보통신부 사업공고 크롤러"""
    
    BASE_URL = "http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList"
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "MSIT")
    
    def fetch_data(self, num_of_rows: int = 100, page_no: int = 1) -> List[Dict[str, Any]]:
        """
        과기부 API에서 데이터를 가져옵니다.
        
        Args:
            num_of_rows: 한 페이지 결과 수 (고정 10)
            page_no: 페이지 번호
            
        Returns:
            원본 데이터 리스트
        """
        try:
            params = {
                "serviceKey": self.api_key,
                "numOfRows": 10,  # API 고정값
                "pageNo": page_no,
                "returnType": "json"
            }
            
            logger.debug(f"🔗 요청 URL: {self.BASE_URL}")
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30
            )
            
            logger.info(f"📨 응답 상태: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            
            # 응답 구조: response > body > items > item
            if isinstance(data, dict) and "response" in data:
                body = data["response"].get("body", {})
                items_wrapper = body.get("items", {})
                
                if isinstance(items_wrapper, dict) and "item" in items_wrapper:
                    items = items_wrapper["item"]
                    # item이 dict면 list로 변환
                    if isinstance(items, dict):
                        return [items]
                    return items if isinstance(items, list) else []
            
            return []
            
        except requests.RequestException as e:
            logger.error(f"❌ API 호출 실패: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"응답 내용: {e.response.text[:500]}")
            return []
    
    def parse_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        과기부 데이터를 통합 형식으로 파싱합니다.
        
        API 필드:
        - subject: 제목
        - deptName: 부서명
        - managerName: 담당자
        - managerTel: 연락처
        - pressDt: 게시일
        - viewUrl: 상세URL
        - files: 첨부파일 (배열)
        """
        # 게시일을 신청 시작일로 사용 (종료일은 없음)
        press_date = self._parse_date(item.get("pressDt"))
        
        return {
            "title": item.get("subject", ""),
            "organization": item.get("deptName", "과학기술정보통신부"),
            "category": "R&D",  # 과기부는 기본적으로 R&D
            "support_type": None,
            "target_audience": None,
            "budget": None,
            "application_start_date": press_date,
            "application_end_date": None,
            "description": None,
            "contact_info": self._format_contact(item),
            "url": item.get("viewUrl", ""),
            "files": self._parse_files(item.get("files", [])),
        }
    
    def _parse_date(self, date_str: Any) -> Any:
        """날짜 문자열을 date 객체로 변환"""
        if not date_str:
            return None
        
        try:
            # "2020-12-10" 형식
            if isinstance(date_str, str):
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_str
        except Exception as e:
            logger.warning(f"⚠️ 날짜 파싱 실패: {date_str} - {e}")
            return None
    
    def _format_contact(self, item: Dict[str, Any]) -> str:
        """연락처 정보를 포맷팅"""
        parts = []
        
        if item.get("managerName"):
            parts.append(f"담당자: {item['managerName']}")
        if item.get("managerTel"):
            parts.append(f"Tel: {item['managerTel']}")
        
        return " | ".join(parts) if parts else None
    
    def _parse_files(self, files: Any) -> List[Dict[str, str]]:
        """첨부파일 정보 파싱"""
        if not files:
            return []
        
        # files가 dict의 file 키를 가진 경우
        if isinstance(files, dict) and "file" in files:
            file_list = files["file"]
            if isinstance(file_list, dict):
                file_list = [file_list]
        elif isinstance(files, list):
            file_list = files
        else:
            return []
        
        result = []
        for file_item in file_list:
            if isinstance(file_item, dict):
                result.append({
                    "fileName": file_item.get("fileName", ""),
                    "fileUrl": file_item.get("fileUrl", "")
                })
        
        return result
