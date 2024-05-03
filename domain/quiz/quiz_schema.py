from pydantic import BaseModel, field_validator

#quiz_entity 테이블
class quiz_eBase(BaseModel):
    id : int
    writer : int
    

class QuizCreate(quiz_eBase):
    type : str
    count : int
    difficulty : str

    @field_validator('title', 'count', 'difficulty')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Quiz_entity(quiz_eBase):

    class Config:
        orm_mode = True
