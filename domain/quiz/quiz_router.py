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
@router.post("", response_model=quiz_schema.quiz_eBase)
async def Create_Quiz_by_Option(quiz_option: quiz_schema.QuizCreate, memo_option: memo_schema.Memo, db: Session = Depends(get_db)):
    quiz_crud.create_quiz(db=db, quiz_option = quiz_option) #퀴즈 옵션 db에 저장
    return memoQuizGroup_crud.create_memo_quiz_group(db=db, Quiz=quiz_option, Memo=memo_option) #퀴즈와 메모 연결한 그룹 DB 저장


