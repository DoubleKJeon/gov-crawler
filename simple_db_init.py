"""
DB 초기화 스크립트 (간단)
"""
import os
import sys

# 환경변수 설정
os.environ["MSIT_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="
os.environ["KSTARTUP_API_KEY"] = "amBxdRMQJ8gJffM8Rkra9XuuZArPGqMo79OVRNQeTg8/utPXFvUNo043qB7EvICpGyai0upwKflNFmIpj/MWYg=="

from app.models import Base
from app.database import engine

print("=" * 60)
print("데이터베이스 초기화")
print("=" * 60)

# 테이블 생성
Base.metadata.create_all(bind=engine)

print("\n✅ 데이터베이스 초기화 완료!")
print("테이블: government_supports")
print("=" * 60)
