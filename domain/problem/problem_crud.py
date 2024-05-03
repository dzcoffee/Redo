from sqlalchemy.orm import Session

from domain.problem.problem_schema import Problem_Create
from models import Problem

async def get_problem_entity(db: Session, id:int):
    # 구현하기

    return

async def create_Problem_entity(db: Session, problem_create: Problem_Create):
    # 구현하기

    return