from pydantic import BaseModel


class MemoQuizGroup(BaseModel):
    id : int
    quiz_id: int
    memo_id: int

    class Config:
        orm_mode = True