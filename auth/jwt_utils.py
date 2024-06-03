from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from utils.logger import logger
from utils.time import kst
import jwt
import time

# OAuth2PasswordBearer를 사용하여 토큰을 추출합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "zvojpryvdipvooazbtfkbjcrhnnumpjwlmbhrvyatjbyevzhjwkyyzgivsxhherq"
ALGORITHM = "HS256"
EXPIRATION_PERIOD = 1440 # 하루

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=403,
        detail="토큰 검증 실패",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 페이로드 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload['exp'] >= datetime.now(kst).timestamp() else None
        
    except jwt.PyJWTError:
        raise credentials_exception

def refresh_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    if payload and payload['exp'] >= datetime.now(kst).timestamp():
        return create_token(payload['userId'])
    return None

def create_token(user_id):
    expiration = datetime.now(kst) + timedelta(minutes=EXPIRATION_PERIOD)
    return jwt.encode({'userId': user_id, 'exp': expiration, 'iss': 'redo'}, SECRET_KEY, algorithm=ALGORITHM)

def get_user(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])['userId']