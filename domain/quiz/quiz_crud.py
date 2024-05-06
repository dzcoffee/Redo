from domain.quiz.quiz_schema import QuizSelect, QuizCreate
from models import Quiz
from sqlalchemy.orm import Session


def get_quiz_option(db: Session):
    quiz_option = db.query(Quiz)\
        .order_by(Quiz.writer.desc())\
        .all()
    return quiz_option


def select_quiz(db: Session, quiz_select: QuizSelect):
    db_quiz = Quiz(count=quiz_select.count, type=quiz_select.type, difficulty=quiz_select.difficulty)
    db.add(db_quiz)
    db.commit()


def get_quiz_id(db: Session, quiz_id: int): #퀴즈 DB모델 자체를 반환하도록 수정하였음
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    return quiz


def create_quiz(db : Session, quiz_option : QuizCreate):
    db_quiz = Quiz(writer = quiz_option.writer, type = quiz_option.type, count = quiz_option.type, difficulty = quiz_option.difficulty )
    db.add(db_quiz)
    db.commit()