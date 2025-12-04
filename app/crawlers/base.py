"""
베이스 크롤러 추상 클래스
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger

from app.models.support import GovernmentSupport


class BaseCrawler(ABC):
    """크롤러 베이스 클래스"""
    
    def __init__(self, api_key: str, source_name: str):
        """
        Args:
            api_key: API 인증 키
            source_name: 데이터 출처 ('MSIT', 'KSTARTUP')
        """
        self.api_key = api_key
        self.source_name = source_name
        logger.info(f"🔧 {source_name} 크롤러 초기화")
    
    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """
        API에서 데이터를 가져옵니다.
        
        Returns:
            원본 데이터 딕셔너리 리스트
        """
        pass
    
    @abstractmethod
    def parse_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        원본 데이터를 통합 형식으로 파싱합니다.
        
        Args:
            item: 원본 데이터 딕셔너리
            
        Returns:
            파싱된 데이터 딕셔너리
        """
        pass
    
    def save_to_db(self, db: Session, parsed_items: List[Dict[str, Any]]) -> int:
        """
        파싱된 데이터를 DB에 저장합니다.
        
        Args:
            db: DB 세션
            parsed_items: 파싱된 데이터 리스트
            
        Returns:
            저장된 아이템 수
        """
        saved_count = 0
        updated_count = 0
        
        for item_data in parsed_items:
            # URL 기반으로 중복 체크
            existing = db.query(GovernmentSupport).filter(
                GovernmentSupport.source_api == self.source_name,
                GovernmentSupport.url == item_data.get("url")
            ).first()
            
            if existing:
                # 기존 데이터 업데이트
                for key, value in item_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                existing.is_new = False  # 기존 공고는 신규 아님
                updated_count += 1
                logger.debug(f"📝 업데이트: {item_data.get('title')[:30]}...")
            else:
                # 신규 데이터 저장
                support = GovernmentSupport(
                    source_api=self.source_name,
                    is_new=True,
                    first_crawled_at=datetime.utcnow(),
                    **item_data
                )
                db.add(support)
                saved_count += 1
                logger.info(f"✨ 신규 공고: {item_data.get('title')[:30]}...")
        
        db.commit()
        logger.success(f"💾 저장 완료: 신규 {saved_count}개, 업데이트 {updated_count}개")
        
        return saved_count
    
    def run(self, db: Session) -> Dict[str, Any]:
        """
        크롤링 전체 프로세스를 실행합니다.
        
        Args:
            db: DB 세션
            
        Returns:
            실행 결과 딕셔너리
        """
        logger.info(f"🚀 {self.source_name} 크롤링 시작")
        
        try:
            # 1. 데이터 가져오기
            raw_items = self.fetch_data()
            logger.info(f"📥 {len(raw_items)}개 데이터 수집")
            
            if not raw_items:
                logger.warning("⚠️ 수집된 데이터가 없습니다")
                return {
                    "success": True,
                    "source": self.source_name,
                    "fetched": 0,
                    "saved": 0,
                    "message": "수집된 데이터 없음"
                }
            
            # 2. 데이터 파싱
            parsed_items = [self.parse_item(item) for item in raw_items]
            
            # 3. DB 저장
            saved_count = self.save_to_db(db, parsed_items)
            
            logger.success(f"✅ {self.source_name} 크롤링 완료")
            
            return {
                "success": True,
                "source": self.source_name,
                "fetched": len(raw_items),
                "saved": saved_count,
                "message": "크롤링 성공"
            }
            
        except Exception as e:
            logger.error(f"❌ {self.source_name} 크롤링 실패: {str(e)}")
            return {
                "success": False,
                "source": self.source_name,
                "error": str(e),
                "message": "크롤링 실패"
            }
