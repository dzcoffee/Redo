from sqlalchemy import Column, Integer, String
from database import Base, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    email = Column(String(128), unique=True)

Base.metadata.create_all(bind=engine)

# 이 코드는 SQLAlchemy를 사용하여 데이터베이스에서 사용자 모델을 정의합니다.
# 사용자 모델에는 사용자의 ID, 사용자 이름, 해시된 비밀번호, 이메일이 포함됩니다.
# 이 모델은 데이터베이스의 "users" 테이블에 매핑됩니다.
