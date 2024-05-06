from domain.problem.problem_schema import Problem_eCreate
from models import Problem
from sqlalchemy.orm import Session


def get_problem_list(db: Session):
    problem_list = db.query(Problem)\
        .order_by(Problem.quizid.desc())\
        .all()
    return problem_list


async def get_problem(db: Session, problem_id: int):
    problem = db.query(Problem).get(problem_id)
    return problem


def create_problem(db: Session, quiz_id : int, question : str, difficulty : str):
    db_problem = Problem(quiz_id = quiz_id, question=question, answer = None, difficulty = difficulty)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem