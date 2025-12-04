"""
설정 (테스트용 - .env 파일 사용 안 함)
"""
import os


class Settings:
    """애플리케이션 설정"""
    
    # Application
    APP_NAME: str = "정부지원사업_크롤러"
    DEBUG: bool = True
    SECRET_KEY: str = "test-secret-key"
    
    # Database
    DATABASE_URL: str = "sqlite:///./gov_support.db"
    
    # API Keys (환경변수에서 읽기)
    MSIT_API_KEY: str = os.getenv("MSIT_API_KEY", "")
    KSTARTUP_API_KEY: str = os.getenv("KSTARTUP_API_KEY", "")
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    EMAIL_ENABLED: bool = False
    
    # JWT
    JWT_SECRET_KEY: str = "test-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    
    # Scheduler
    CRAWLER_CRON: str = "0 0 * * *"
    SCHEDULER_ENABLED: bool = False
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = "logs/app.log"


# 싱글톤 인스턴스
settings = Settings()
