from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接 URL
# 데이터베이스 연결 URL
DATABASE_URL = "sqlite:///./user.db"

# 创建引擎
# 엔진 생성
engine = create_engine(DATABASE_URL)

# 创建 SessionLocal 会话
# Create SessionLocal 세션
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()

# 이 코드는 데이터베이스에 연결하고 SQLAlchemy의 sessionmaker를 사용하여 데이터베이스 세션을 만듭니다.
