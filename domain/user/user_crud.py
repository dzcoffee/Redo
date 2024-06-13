from sqlalchemy.orm import Session
from domain.user.user_schema import UserDto
from models import User

from utils.logger import logger
from utils.password import password_context

def create_user(db: Session, user_create: UserDto):
    db_user = User(nickname=user_create.nickname,
                   password=password_context.hash(user_create.password),
                   accountID=user_create.accountID)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserDto):
    return db.query(User).filter(
        (User.nickname == user_create.nickname) |
        (User.accountID == user_create.accountID) #???
    ).first()

def get_all_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

