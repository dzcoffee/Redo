from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models, schemas, security, database
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = security.get_password_hash(user.password)

    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"access_token": security.create_access_token(data={"sub": user.username}), "token_type": "bearer"}


@app.post("/token", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user or not security.verify_password(user_credentials.password, user.hashed_password):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
