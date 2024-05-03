from pydantic import BaseModel, field_validator

#problem_entity 테이블
class problem(BaseModel):
    id : int
    quizid : int
    

class Problem_eCreate(problem):
    question : str
    difficulty : str

    @field_validator('question', 'difficulty')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Problem_entity(problem):
    answer : str
    class Config:
        orm_mode = True