from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from auth.auth import authenticate_user
from auth.jwt_utils import create_token
from utils.logger import logger

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/user",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.post("/login", response_model=user_schema.AuthResponse)
async def get_auth_token(auth_request: user_schema.AuthRequest, db: Session = Depends(get_db)):
    retrieved_user = authenticate_user(db, auth_request)
    if not retrieved_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect id or password"
        )
    token = create_token(retrieved_user.id)
    return user_schema.AuthResponse(nickname=retrieved_user.nickname, access_token=token)