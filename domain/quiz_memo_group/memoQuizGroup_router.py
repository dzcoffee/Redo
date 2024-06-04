from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from auth.auth_validator import AuthValidator
from domain.quiz_memo_group import memoQuizGroup_crud, memoQuizGroup_schema

router = APIRouter(
    prefix="/memoQuizGroup",
    dependencies=[Depends(AuthValidator())],
    tags=["퀴즈"]
)


@router.get("/{memo_id}", response_model=memoQuizGroup_schema.MemoQuizGroup,description="메모 아이디 조회")
async def memo(memo_id: int, db: Session = Depends(get_db)):
    memo = await memoQuizGroup_crud.get_memoId(db, memo_id=memo_id)
    memo_quiz_group = memoQuizGroup_schema.MemoQuizGroup(quizid=memo.quizid, memoid=memo.memoid)
    return memo_quiz_group.dict()


@router.get("/{quiz_id}", response_model=memoQuizGroup_schema.MemoQuizGroup,description="퀴즈 아이디 조회")
async def quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = await memoQuizGroup_crud.get_quizId(db, quiz_id=quiz_id)
    memo_quiz_group = memoQuizGroup_schema.MemoQuizGroup(quizid=quiz.quizid, memoid=quiz.memoid)
    return memo_quiz_group.dict()

"""""
@router.post("/", response_model=memoQuizGroup_schema.MemoQuizGroup, description="Memo와 Quiz를 연결")
def create_memo_quiz_group(memo_id: int, quiz_id: int, db: Session = Depends(get_db)):
    memo_quiz_group = memoQuizGroup_crud.create_memo_quiz_group(db, memo_id=memo_id, quiz_id=quiz_id)
    if not memo_quiz_group:
        raise HTTPException(status_code=404, detail="Memo or Quiz not found")
    return memo_quiz_group
"""