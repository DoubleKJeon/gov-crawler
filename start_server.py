"""
서버 실행 (환경변수 방식)
"""
import os

# 환경변수 설정
os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
os.environ["DEBUG"] = "True"
os.environ["SCHEDULER_ENABLED"] = "False"
os.environ["EMAIL_ENABLED"] = "False"
os.environ["REDIS_ENABLED"] = "False"

# config_simple을 config로 대체
import sys
from app import config_simple
sys.modules['app.config'] = config_simple

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("서버 시작 중...")
    print("=" * 60)
    print()
    print("Swagger UI: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print()
    print("Ctrl+C로 종료")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
