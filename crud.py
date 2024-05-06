from sqlalchemy.orm import Session
from . import models, schemas, security

# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)  # 密码加密
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 获取用户通过用户名
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# 获取所有用户
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 更新用户
def update_user(db: Session, username: str, update_fields: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db_user.email = update_fields.email if update_fields.email else db_user.email
        if update_fields.password:
            db_user.hashed_password = security.get_password_hash(update_fields.password)
        db.commit()
        db.refresh(db_user)
    return db_user

# 删除用户
def delete_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
