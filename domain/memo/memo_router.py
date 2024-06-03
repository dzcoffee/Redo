from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.memo import memo_schema, memo_crud
from auth.auth import user_from_request
from auth.auth_validator import AuthValidator

from utils.logger import logger
# import logging

# logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/memo",
    dependencies=[Depends(AuthValidator())]
)


# Deprecated 예정
@router.get("", response_model=list[memo_schema.Memo], description="메모 메인(목록) 페이지")
#memo_list 함수의 리턴값은 Memo 스키마로 구성된 리스트
def memo_list(request: Request, db: Session = Depends(get_db)):
    userId = user_from_request(request)
    logger.info(userId)
    _memo_list = memo_crud.get_memo_by_user(db, userId)
    return _memo_list


@router.get("/{memo_id}", response_model=memo_schema.Memo, description="메모 조회 페이지")
def memo_detail(memo_id: int, request: Request, db: Session = Depends(get_db)):
    userId = user_from_request(request)
    memo = memo_crud.get_memo(db, memo_id=memo_id)
    if userId != memo.writer:
        raise HTTPException(status_code=401, detail="Incorrect user")
    return memo

# TODO: JWT 인증 구현시 request 제거 -> JWT 페이로드의 유저 ID로 대체
@router.post("/user", response_model=list[memo_schema.Memo], description="메모 검색 페이지")
async def memo_by_user(request: memo_schema.MemoByUserRequest, db: Session = Depends(get_db)):
    memo_list = memo_crud.get_memo_by_user(db, writer=request.writer)
    return memo_list

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, description="메모 생성 페이지")
async def memo_create( _memo_create: memo_schema.MemoCreate,
                    db: Session = Depends(get_db)):
    await memo_crud.create_memo(db=db, memo_create=_memo_create)






