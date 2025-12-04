"""
스케줄러
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from app.config import settings
from app.database import SessionLocal
from app.crawlers import MSITCrawler, KStartupCrawler


class CrawlerScheduler:
    """크롤러 스케줄러"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.running = False
    
    def daily_crawl(self):
        """매일 크롤링 작업"""
        logger.info("🕐 스케줄 크롤링 시작")
        
        db = SessionLocal()
        try:
            results = []
            
            # MS

IT 크롤러
            msit = MSITCrawler(settings.MSIT_API_KEY)
            result_msit = msit.run(db)
            results.append(result_msit)
            
            # K-Startup 크롤러
            kstartup = KStartupCrawler(settings.KSTARTUP_API_KEY)
            result_kstartup = kstartup.run(db)
            results.append(result_kstartup)
            
            logger.success("✅ 스케줄 크롤링 완료")
            return results
            
        except Exception as e:
            logger.error(f"❌ 스케줄 크롤링 실패: {e}")
            return None
        finally:
            db.close()
    
    def start(self):
        """스케줄러 시작"""
        if not settings.SCHEDULER_ENABLED:
            logger.warning("⚠️ 스케줄러가 비활성화되어 있습니다")
            return
        
        # Cron 스케줄 설정
        self.scheduler.add_job(
            self.daily_crawl,
            CronTrigger.from_crontab(settings.CRAWLER_CRON),
            id="daily_crawler",
            name="일일 정부지원사업 크롤링",
            replace_existing=True
        )
        
        self.scheduler.start()
        self.running = True
        logger.info(f"✅ 스케줄러 시작: {settings.CRAWLER_CRON}")
    
    def shutdown(self):
        """스케줄러 종료"""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            logger.info("⏹ 스케줄러 종료")


# 싱글톤 인스턴스
scheduler = CrawlerScheduler()
