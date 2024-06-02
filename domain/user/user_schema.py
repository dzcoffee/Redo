from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    accountID: str
    nickname: str
    password: str


    @field_validator('nickname', 'password', 'accountID')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class AuthRequest(BaseModel):
    accountID: str
    password: str


class Token(BaseModel):
    access_token: str
