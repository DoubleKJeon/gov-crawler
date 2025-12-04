"""
로거 설정
"""
import sys
from pathlib import Path
from loguru import logger

from app.config import settings


def setup_logger():
    """Loguru 로거 설정"""
    
    # 기존 핸들러 제거
    logger.remove()
    
    # 콘솔 출력
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        colorize=True,
    )
    
    # 파일 출력
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
    )
    
    logger.info("✅ 로거 초기화 완료")
    
    return logger
