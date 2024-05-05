from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models, schemas, security, database
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

# 获取数据库session的依赖
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建用户的路由
@app.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 检查用户名是否已注册
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # 将密码哈希化
    hashed_password = security.get_password_hash(user.password)
    # 创建用户
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"access_token": security.create_access_token(data={"sub": user.username}), "token_type": "bearer"}

# 登录获取访问令牌的路由
@app.post("/token", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        # 如果用户不存在或密码不匹配，返回401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
# 이 코드는 FastAPI를 사용하여 사용자 등록 및 로그인을 처리하는 방법을 보여줍니다.
# 사용자 등록 시 사용자 이름의 중복을 확인하고, 비밀번호를 해싱하여 저장합니다.
# 로그인 시 제출된 사용자 이름과 비밀번호를 검증하고, 인증되면 액세스 토큰을 생성하여 반환합니다.
