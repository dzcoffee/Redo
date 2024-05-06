from pydantic import BaseModel

# 用户创建请求模型
class UserCreate(BaseModel):
    
    username: str
    email: str
    password: str

# 用户登录请求模型
class UserLogin(BaseModel):
    
    username: str
    password: str

# 用于响应的Token模型
class Token(BaseModel):
    
    access_token: str
    token_type: str

# 이 코드는 Pydantic을 사용하여 사용자의 요청 및 응답 모델을 정의합니다.
# UserCreate 모델은 사용자가 생성할 때 요청하는 데이터를 정의하고,
# UserLogin 모델은 사용자가 로그인할 때 요청하는 데이터를 정의합니다.
# Token 모델은 응답에 대한 토큰을 정의합니다.
