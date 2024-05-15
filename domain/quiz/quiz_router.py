from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session
from starlette import status

from database import get_db

from domain.quiz import quiz_schema, quiz_crud
from domain.memo import memo_schema, memo_crud
from domain.quiz_memo_group import memoQuizGroup_crud, memoQuizGroup_schema

router = APIRouter(
    prefix="/quiz",
)

#퀴즈 옵션 선택한 거 받아와서 DB에 새로 생성하는 api
@router.post("", response_model=memoQuizGroup_schema.MemoQuizGroup)
async def Create_Quiz_by_Option(quiz_count:int, difficulty:str, memoID : int, type : str, db: Session = Depends(get_db)):
    db_quiz = quiz_crud.create_quiz(db=db, type = type, quiz_count = quiz_count, difficulty = difficulty ) #퀴즈 옵션 db에 저장
    print(db_quiz.id)
    return memoQuizGroup_crud.create_memo_quiz_group(db=db, memo_id = memoID, quiz_id=db_quiz.id) #퀴즈와 메모 연결한 그룹 DB 저장


