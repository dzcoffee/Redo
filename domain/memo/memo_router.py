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
    tags=["메모"],
    dependencies=[Depends(AuthValidator())]
)

# 요청한 사용자와 메모 등록자가 동일한 경우에만 메모를 반환
# 그렇지 않으면 401 에러 발생
def safe_get_memo(request: Request, memo_id: int, db: Session = Depends(get_db)):
    user_id = user_from_request(request)
    memo = memo_crud.get_memo(db, memo_id=memo_id)
    if user_id != memo.writer:
        raise HTTPException(status_code=401, detail="Incorrect user")
    return memo

@router.get("/all-dev-only", response_model=list[memo_schema.Memo], description="전체 메모 조회")
def get_all_memo(db: Session=Depends(get_db)):
    return memo_crud.get_memo_list(db)

@router.get("", response_model=list[memo_schema.Memo], description="메모 메인(목록) 페이지")
def memo_by_user(request: Request, db: Session = Depends(get_db)):
    user_id = user_from_request(request)
    logger.info(f'user_id: {user_id}')
    _memo_list = memo_crud.get_memo_by_user(db, user_id)
    return _memo_list


@router.get("/{memo_id}", response_model=memo_schema.Memo, description="메모 조회 페이지")
def memo_detail(memo_id: int, request: Request, db: Session = Depends(get_db)):
    return safe_get_memo(request, memo_id, db)

@router.post("/create", status_code=status.HTTP_201_CREATED, description="메모 생성 페이지")
async def memo_create( _memo_create: memo_schema.MemoCreate, request: Request,
                    db: Session = Depends(get_db)):
    user_id = user_from_request(request)
    await memo_crud.create_memo(db=db, memo_create=_memo_create, user_id=user_id)

@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT, description="메모 삭제 페이지")
async def memo_delete(memo_id: int, request: Request, db: Session = Depends(get_db)):
    # 요청한 사용자와 메모 등록자가 같은지 확인
    safe_get_memo(request, memo_id, db)
    memo_crud.delete_memo(db, memo_id)



