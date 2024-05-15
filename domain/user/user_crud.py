from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(nickname=user_create.nickname,
                   password=pwd_context.hash(user_create.password),
                   accountID=user_create.accountID)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.nickname == user_create.nickname) |
        (User.accountID == user_create.accountID) #???
    ).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

