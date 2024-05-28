from datetime import datetime

import openai

from domain.memo.memo_schema import MemoCreate
from models import Memo
from sqlalchemy.orm import Session

async def moderate_text(text: str):
    response = await openai.Moderation.create(input=text)
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


async def create_memo(db: Session, memo_create: MemoCreate):
    moderation_result = await moderate_text(memo_create.content)
    if moderation_result["flagged"]: #flagged==True
        # 모데레이션 부적절 감지
        return {"error": "Inappropriate content detected"}

    #모데레이션 적용 후 메모 생성
    db_memo = Memo(title=memo_create.title, content=memo_create.content,
                           createAt=datetime.now())
    db.add(db_memo)
    db.commit()





