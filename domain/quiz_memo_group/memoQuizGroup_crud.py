from models import Memo
from models import Quiz
from models import MemoQuizGroup
from sqlalchemy.orm import Session
from domain.memo import memo_crud
from domain.quiz import quiz_crud


def get_memoId(db: Session, quiz_id: int): #quiz_id로 memo_id 찾아주기
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    return quiz


def get_quizId(db: Session, memo_id: int): #memo_id로 quiz_id 찾아주기
    memo = db.query(Memo).get(memo_id)

    return memo


def create_memo_quiz_group(db: Session, memo_id: int, quiz_id: int): #값 반환함. -> refresh해서 최신정보 줌
    memo_quiz_group = MemoQuizGroup(memo_id=memo_id, quiz_id=quiz_id)
    db.add(memo_quiz_group)
    db.commit()
    db.refresh(memo_quiz_group)
    return memo_quiz_group
    