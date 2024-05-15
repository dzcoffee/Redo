import datetime

from pydantic import BaseModel, field_validator


class Memo(BaseModel):
    id: int
    title: str
    content: str
    createAt: datetime.datetime

    class Config:
        orm_mode=True


class MemoCreate(BaseModel):
    title: str
    content: str

    @field_validator('title', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v



