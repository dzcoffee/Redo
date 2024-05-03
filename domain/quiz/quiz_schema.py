from pydantic import BaseModel, field_validator

#quiz_entity 테이블
class quiz_eBase(BaseModel):
    id : int
    writer : int
    

class QuizCreate(quiz_eBase):
    type : str
    count : int
    difficulty : str

class Quiz_entity(quiz_eBase):

    class Config:
        orm_mode = True
