from domain.problem.problem_schema import Problem_eCreate
from models import Problem
from sqlalchemy.orm import Session
import json

from typing import List

def get_problem_list(db: Session):
    problem_list = db.query(Problem)\
        .order_by(Problem.quizid.desc())\
        .all()
    return problem_list


def get_problem(db: Session, problem_id: int):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    return problem


def create_problem(db: Session, quiz_id : int, question : str, difficulty : str, options : json, answer: str, comentary : str):
    db_problem = Problem(quizid = quiz_id, question=question, answer = answer, options=options, difficulty = difficulty, comentary = comentary)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

def get_feedback(db: Session, problem_id: int):
    db_problem = db.query(Problem).get(problem_id)
    if db_problem:
        return db_problem.feedback
    return None

def delete_problem(db: Session, problem_id: int):
    db_problem = db.query(Problem).get(problem_id)
    if db_problem:
        if db_problem.feedback < 4:
            db.delete(db_problem)
            db.commit()
        return db_problem
    return None

def delete_problem_if_low_feedback(db: Session, problem_id: int, feedback: int):
    db_problem = db.query(Problem).get(problem_id)
    if db_problem and feedback <= 7:
        db.delete(db_problem)
        db.commit()
        return True
    return False
