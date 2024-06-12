from pydantic import BaseModel, field_validator
from typing import Optional, List

#problem_entity 테이블
class problem(BaseModel):
    id : int
    quizid : Optional[int]
    question : str
    difficulty : Optional[str]
    answer : Optional[str]
    options : Optional[List[str]]
    comentary : Optional[str]
    correctness : Optional[int]


class Problem_eCreate(problem):
    

    @field_validator('question', 'difficulty')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Problem_entity(problem):
    
    class Config:
        orm_mode = True