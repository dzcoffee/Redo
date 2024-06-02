from sqlalchemy.orm import Session
from domain.user.user_schema import AuthRequest
from models import User
from passlib.context import CryptContext

from utils.logger import logger

# 사용자 인증 및 토큰 생성

# 사용자 인증 함수
def authenticate_user(db: Session, request: AuthRequest):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = db.query(User).filter(User.accountID == request.accountID).first()
    logger.info(f'Query User: {user}')
    if not user or not pwd_context.verify(request.password, user.password):
        return False
    return user