from fastapi import Request
from sqlalchemy.orm import Session
from domain.user.user_schema import AuthRequest
from models import User

from auth.jwt_utils import get_user
from utils.logger import logger
from utils.password import password_context

# 사용자 인증 및 토큰 생성

# 사용자 인증 함수
def authenticate_user(db: Session, request: AuthRequest):
    user = db.query(User).filter(User.accountID == request.accountID).first()
    logger.info(f'Query User: {user}')
    if not user or not password_context.verify(request.password, user.password):
        return False
    return user

# 요청 데이터에서 사용자 정보 얻기
def user_from_request(request: Request):
    token = request.state.access_token
    if not token:
        return None
    
    return get_user(token)