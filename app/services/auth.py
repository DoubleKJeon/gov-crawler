"""
인증 서비스
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, TokenData

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰 생성"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """JWT 토큰 디코딩"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            return None
        
        return TokenData(email=email)
    except JWTError:
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """사용자 인증"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def create_user(db: Session, user_create: UserCreate) -> User:
    """사용자 생성"""
    # 이메일 중복 체크
    existing = db.query(User).filter(User.email == user_create.email).first()
    if existing:
        raise ValueError("이미 사용 중인 이메일입니다")
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(user_create.password)
    
    # 사용자 생성
    user = User(
        email=user_create.email,
        password_hash=hashed_password,
        name=user_create.name,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def update_last_login(db: Session, user: User) -> None:
    """마지막 로그인 시간 업데이트"""
    user.last_login = datetime.utcnow()
    db.commit()
