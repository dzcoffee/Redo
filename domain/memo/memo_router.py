from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.memo import memo_schema, memo_crud

import openai

import pandas as pd
import os

# import logging

# logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/memo",
)

openai.api_key = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"
model = 'text-embedding-3-small'

@router.get("", response_model=list[memo_schema.Memo], description="메모 메인(목록) 페이지")
#memo_list 함수의 리턴값은 Memo 스키마로 구성된 리스트
def memo_list(db: Session = Depends(get_db)):
    _memo_list = memo_crud.get_memo_list(db)
    return _memo_list


@router.get("/{memo_id}", response_model=memo_schema.Memo, description="메모 조회 페이지")
def memo_detail(memo_id: int, db: Session = Depends(get_db)):
    memo = memo_crud.get_memo(db, memo_id=memo_id)
    return memo


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, description="메모 생성 페이지")
def memo_create( _memo_create: memo_schema.MemoCreate,
                    db: Session = Depends(get_db)):
    
    embeddings_memo = _memo_create.content
    res = openai.embeddings.create(
                input = embeddings_memo,
                model = 'text-embedding-3-small'
    )

    embedding = res.data[0].embedding

    data_list = []

    data_list.append({
        'memo_title' : _memo_create.title,
        #'category' : _memo_create.category <<< 카테고리 관련 DB 구성되면 활성화
        'embeddings' : embedding
    })

    print(data_list)

    user_Id = 1 #임시로 받은 user_id값임. 로그인 기능 등 user_id 관련된 것 받아와야 함
    file_path = f"./{user_Id}_memo.csv"

    csv_save(file_path, data_list)

    memo_crud.create_memo(db=db, memo_create=_memo_create)



def csv_save(file_path, data_list):
    # 데이터프레임 생성
    df = pd.DataFrame(data_list)

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




