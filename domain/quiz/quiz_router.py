from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session
from starlette import status

from database import get_db

from domain.quiz import quiz_schema, quiz_crud
from domain.memo import memo_schema, memo_crud
from domain.quiz_memo_group import quiz_memo_group_schema, quiz_memo_group_crud

router = APIRouter(
    prefix="/quiz",
)

#DB로부터 메모 목록 받아오는 api
@router.get("") 
async def Get_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> dict:
    db_memos = memo_crud.get_memo(db, skip=skip, limit=limit)
    if db_memos is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    return db_memos

#퀴즈 옵션 선택한 거 받아와서 DB에 새로 생성하는 api
@router.post("", response_model=quiz_schema.quiz_eBase)
async def Create_Quiz_by_Option(quiz_option: quiz_schema.QuizCreate, memo_option: memo_schema.Memo, db: Session = Depends(get_db)):
    quiz_crud.create_quiz(db=db, quiz_option = quiz_option) #퀴즈 옵션 저장
    return quiz_memo_group_crud.create_problem_group(db=db, Quiz=quiz_option, Memo=memo_option) #퀴즈와 메모 연결한 그룹 DB 저장


