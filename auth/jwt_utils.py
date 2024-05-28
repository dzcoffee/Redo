from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from domain.security.token_schema import TokenData
from datetime import datetime, timedelta
from utils.logger import logger
import jwt

# OAuth2PasswordBearer를 사용하여 토큰을 추출합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "zvojpryvdipvooazbtfkbjcrhnnumpjwlmbhrvyatjbyevzhjwkyyzgivsxhherq"
ALGORITHM = "HS256"
EXPIRATION_PERIOD = 30 # 30분

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="토큰 검증 실패",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 페이로드 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        # username이 없으면 예외를 발생시킵니다.
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        # 토큰 디코딩 중 오류가 발생하면 예외를 발생시킵니다.
        raise credentials_exception
    
    # 검증된 토큰 데이터를 반환합니다.
    return token_data

def create_token(user_id):
    expiration = datetime.now() + timedelta(minutes=EXPIRATION_PERIOD)
    return jwt.encode({'accountId': user_id, 'exp': expiration, 'iss': 'redo'}, SECRET_KEY, algorithm=ALGORITHM)