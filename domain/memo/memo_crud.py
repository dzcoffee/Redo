from datetime import datetime

import openai

from domain.memo.memo_schema import MemoCreate
from models import Memo
from utils.logger import logger
from sqlalchemy.orm import Session

async def moderate_text(text: str):
    response = openai.Moderation.create(input=text)
    logger.info(f"Moderation response: {response}")
    return response['results'][0]

def get_memo_list(db: Session):
    memo_list = db.query(Memo)\
        .order_by(Memo.createAt.desc())\
        .all()
    return memo_list


def get_memo(db: Session, memo_id: int):
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    return memo

def get_memo_by_user(db: Session, writer: int):
    memo_list = db.query(Memo).filter(Memo.writer == writer).all()
    return memo_list

def delete_memo(db: Session, memo_id: int):
    db.query(Memo).filter(Memo.id == memo_id).delete()
    db.commit()


async def create_memo(db: Session, memo_create: MemoCreate, user_id: str):
    moderation_result = await moderate_text(memo_create.content)
    logger.info(f"Moderation result: {moderation_result}")
    if moderation_result["flagged"]: #flagged==True
        # 모데레이션 부적절 감지
        return {"error": "Inappropriate content detected"}

    #모데레이션 적용 후 메모 생성
    db_memo = Memo.from_dto(memo_create, user_id)
    logger.info(f"Memo created: {db_memo}")
    db.add(db_memo)
    db.commit()

    return db_memo.id  # 방금 생성된 메모의 ID 반환
    





