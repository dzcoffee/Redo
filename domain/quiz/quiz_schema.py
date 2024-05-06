from pydantic import BaseModel, field_validator

#quiz_entity 테이블
class quiz_eBase(BaseModel):
    id : int
    writer : int
    type : str
    count : int
    difficulty : str

    class Config:
        orm_mode = True
    

class QuizCreate(quiz_eBase):
    pass

class QuizSelect(BaseModel):
    count: int
    type: str
    difficulty: str

    @field_validator('count', 'type', 'difficulty')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v