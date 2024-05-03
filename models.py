from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

from database import Base


class Memo(Base):
    __tablename__ = "memo"

    id = Column(Integer, primary_key=True)
    writer = Column(Integer, ForeignKey('user.id'))
    categories = Column(Text)  # VARCHAR로 축소하는 게 좋지 않은가?
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    createAt = Column(DateTime, nullable=False)

  #  user_entity = relationship("User_entity", back_populates="memo_entities")
   # problem_groups = relationship("Problem_group", back_populates="memo_entity")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(VARCHAR(10), unique=True
                      )
    accountID = Column(VARCHAR(20), unique=True)
    password = Column(VARCHAR(30))



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


class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quizid = Column(Integer, ForeignKey('quiz.id'))
    question = Column(Text)
    answer = Column(Text)
    difficulty = Column(VARCHAR(20), ForeignKey('quiz.difficulty'))


class MemoQuiz_group(Base):
    __tablename__ = "memo_quiz_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quizid = Column(Integer, ForeignKey('quiz.id'))
    memoid = Column(Integer, ForeignKey('memo.id'))