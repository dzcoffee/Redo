from datetime import datetime

from openai import OpenAI
import openai
import logging
from domain.memo.memo_schema import MemoCreate
from models import Memo
from utils.logger import logger
from sqlalchemy.orm import Session

OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"


client = OpenAI(
    api_key=OPENAI_API_KEY
)

def moderate_text(text: str):
    logger.info(f"Original text: {text}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Translate to English."},
            {"role": "user", "content": text},
        ]
    )
    translated_text = response.choices[0].message.content
    logger.info(f"translated response: {translated_text}")
    response = client.moderations.create(input=translated_text)
    logger.info(f"Moderation response: {response}")
    return response.results[0]

def get_memo_list(db: Session):
    memo_list = db.query(Memo)\
        .order_by(Memo.createAt.desc())\
        .all()
    return memo_list


def get_memo(db: Session, memo_id: int):
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    memo.categories = memo.categories.split(',')
    return memo

def get_memo_by_user(db: Session, writer: int):
    memo_list = db.query(Memo).filter(Memo.writer == writer).all()
    for memo in memo_list:
        memo.categories = memo.categories.split(',')
    return memo_list

def update_memo(db: Session, memo: Memo, dto: MemoCreate):
    memo.title = dto.title
    memo.categories = ','.join(dto.categories)
    memo.content = dto.content
    db.commit()
    db.refresh(memo)

def delete_memo(db: Session, memo_id: int):
    db.query(Memo).filter(Memo.id == memo_id).delete()
    db.commit()


def create_memo(db: Session, memo_create: MemoCreate, user_id: str):
    moderation_result = moderate_text(memo_create.content)
    logger.info(f"Moderation result: {moderation_result}")
    if moderation_result.flagged: #flagged==True
        # 모데레이션 부적절 감지
        flag = 'Mod'
        return flag

    #모데레이션 적용 후 메모 생성
    db_memo = Memo.from_dto(memo_create, user_id)
    logger.info(f"Memo created: {db_memo}")
    db.add(db_memo)
    db.commit()

    return db_memo.id  # 방금 생성된 메모의 ID 반환
    






