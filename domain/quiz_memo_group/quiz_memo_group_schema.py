from pydantic import BaseModel

#problem_group 테이블
class MemoQuiz_gBase(BaseModel):
    id : int
    quizid : int
    memoid : int

class MemoQuiz_gCreate(MemoQuiz_gBase):
    pass

class MemoQuiz_group(MemoQuiz_gBase):
    class Config:
        orm_mode = True