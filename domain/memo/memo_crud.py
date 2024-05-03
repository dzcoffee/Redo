from datetime import datetime

from domain.memo.memo_schema import MemoCreate
from models import Memo
from sqlalchemy.orm import Session


def get_memo_list(db: Session):
    memo_list = db.query(Memo)\
        .order_by(Memo.createAt.desc())\
        .all()
    return memo_list


async def get_memo(db: Session, memo_id: int):
    memo = db.query(Memo).get(memo_id)
    return memo


def create_memo(db: Session, memo_create: MemoCreate):
    db_memo = Memo(title=memo_create.title, content=memo_create.content,
                           createAt=datetime.now())
    db.add(db_memo)
    db.commit()





