from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.memo import memo_schema, memo_crud
from auth.auth import user_from_request
from auth.auth_validator import AuthValidator

import openai

import pandas as pd
import os

from utils.logger import logger

from openai import OpenAI
import openai

import pandas as pd
import os
# import logging

# logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.INFO)


OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"
from openai import OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)


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

    memo_id = memo_crud.create_memo(db=db, memo_create=_memo_create, user_id=user_id)

    if memo_id == 'Mod':
        return {"error": "Inappropriate content detected"}

    embeddings_memo = _memo_create.content
    print("임베딩전메모\n")
    print(embeddings_memo)

    res = client.embeddings.create(
        input = embeddings_memo,
        model = 'text-embedding-3-small'
    )

    embedding = res.data[0].embedding

    data_list = []

    data_list.append({
        'id' : memo_id,
        'embeddings' : embedding
    })

    #print(data_list)

    file_path = f"memo_csv/{user_id}_memo.csv"

    csv_save(file_path, data_list)


def csv_save(file_path, data_list):
    # 데이터프레임 생성
    df = pd.DataFrame(data_list)

    #print(data_list)
    # 파일이 존재하는지 확인
    if os.path.exists(file_path):
        # 파일이 존재하면 기존 데이터를 읽어옵니다.
        existing_df = pd.read_csv(file_path)
        # 새로운 데이터프레임을 기존 데이터에 추가합니다.
        df = pd.concat([existing_df, df], ignore_index=True)
    else:
        print(f"{file_path} 파일이 존재하지 않으므로 새로 생성합니다.")

    # 데이터프레임을 CSV 파일에 저장
    df.to_csv(file_path, index=False)

    print(f"데이터가 {file_path}에 저장되었습니다.")
    



@router.patch("/{memo_id}", status_code=status.HTTP_200_OK, description="메모 내용 변경")
async def memo_update(memo_id: int, dto: memo_schema.MemoCreate, request: Request, db: Session = Depends(get_db)):
    original_memo = safe_get_memo(request, memo_id, db)
    return memo_crud.update_memo(db, original_memo, dto)


@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT, description="메모 삭제 페이지")
async def memo_delete(memo_id: int, request: Request, db: Session = Depends(get_db)):
    # 요청한 사용자와 메모 등록자가 같은지 확인
    safe_get_memo(request, memo_id, db)
    memo_crud.delete_memo(db, memo_id)