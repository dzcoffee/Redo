
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, VARCHAR, JSON
from database import Base
from datetime import datetime

from domain.memo.memo_schema import MemoCreate
from utils.time import kst


class Memo(Base):
    __tablename__ = "memo"

    id = Column(Integer, primary_key=True)
    writer = Column(Integer, ForeignKey('user.id'))
    categories = Column(Text)  # VARCHAR로 축소하는 게 좋지 않은가?
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    createAt = Column(DateTime, nullable=False)

    @staticmethod
    def from_dto(dto: MemoCreate, user_id: str):
        return Memo(
            writer=user_id,
            categories=",".join(dto.categories) if dto.categories else "",
            title= dto.title,
            content=dto.content,
            createAt=datetime.now(kst)
        )

    def __str__(self):
        return f'Memo(id={self.id}, title={self.title}, categories={self.categories}, content={self.content})'

  #  user_entity = relationship("User_entity", back_populates="memo_entities")
   # problem_groups = relationship("Problem_group", back_populates="memo_entity")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(VARCHAR(10), unique=True
                      )
    accountID = Column(VARCHAR(20), unique=True)
    password = Column(VARCHAR(30))

    def __str__(self):
        return f'User(id={self.id}, nickname={self.nickname}, accountID={self.accountID}, password={self.password})'



  #  quiz_entities = relationship("Quiz_entity", back_populates="user_entity")
   # memo_entities = relationship("Memo_entity", back_populates="user_entity")
#

class Quiz(Base):
    __tablename__ = "quiz"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    writer = Column(Integer, ForeignKey('user.id'))
    type = Column(VARCHAR(30))
    count = Column(Integer)
    difficulty = Column(VARCHAR(20))

    # user = relationship("User", back_populates="quiz")
    # problem = relationship("Problem", back_populates="quiz")
    # problem_groups = relationship("Problem_group", back_populates="quiz")


class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quizid = Column(Integer, ForeignKey('quiz.id'))
    question = Column(Text)
    answer = Column(Text)
    difficulty = Column(VARCHAR(20), ForeignKey('quiz.difficulty'))
    options = Column(JSON)
    comentary = Column(Text) #해설용

    #quiz = relationship("Quiz", back_populates="problem")


class MemoQuizGroup(Base):
    __tablename__ = "memoQuizGroup"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer)
    memo_id = Column(Integer)
    #memo = relationship("Memo")
    #quiz = relationship("Quiz")
