from fastapi import APIRouter, Depends, HTTPException

from openai import OpenAI

from database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

import json

from domain.memo import memo_schema, memo_crud
from domain.quiz import quiz_schema, quiz_crud
from domain.quiz_memo_group import memoQuizGroup_schema, memoQuizGroup_crud
from domain.problem import problem_schema, problem_crud

from pydantic import BaseModel


OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"

client = OpenAI(
    api_key = OPENAI_API_KEY
)

MODEL = "gpt-4-turbo" #json형식 return 받으려면 1106버전 이상 

DB_Problem_List = []

router = APIRouter(
    prefix="/quiz/game",
)

#선택한 옵션으로 gpt api를 통해 생성된 문제를 쏴주는 api
@router.get("/{quiz_id}", response_model=List[problem_schema.problem]) # << Problem entity Pydantic모델의 리스트로 리턴받음. ##, response_model=List[Problem]## 추가할 것
async def Create_problems(quiz_id: int, db: Session = Depends(get_db)):
    
    ##quiz_id로 quiz 정보 db에 요청
    db_quiz = quiz_crud.get_quiz_id(db, quiz_id)

    ##quiz_id로 묶인 memo 정보 db에 요청
    db_memo= memoQuizGroup_crud.get_memoId(db, quiz_id) ## 이거 내부 코드 수정을 해야됨.

    if db_memo is None:
    # 적절한 예외 처리나 오류 메시지 반환
        raise HTTPException(status_code=404, detail="Memo not found")

    model = MODEL 

    query = f"{db_memo.content}라는 내용을 바탕으로 {db_quiz.type}형태로, {db_quiz.count}개의 문제를 만들어줄래?" #json 형태 반환 시 json이 query에 포함되어 있어야함
    #difficulty는 일단 제외 테스트 후 추가

    messages = [{"role": "system","content": "You are a helpful quiz maker system and also verify user answers and speak Korean "}, 
                {"role": "user","content": query},
                {"role": "system", "content" : "The output format should be as follows'. The number of quesiton follow in the user input. You must not say 'any other things' before 'Question'. Also you must input Separtor '==========!!' between each Qusetion. If type is '단답식', please answer without options.'\n"
                 +"Format:\n"
                 +"{Question}?"
                 +"==========!!\n"
                 + "@!@!@!@{Option1} "
                 + "@!@!@!@{Option2} "
                 + "@!@!@!@{Option3} "
                 + "@!@!@!@{Option4} "
                 +"==========!!"
                 + "{Question}?"
                 +"==========!!\n"
                 + "@!@!@!@{Option1} "
                 + "@!@!@!@{Option2} "
                 + "@!@!@!@{Option3} "
                 + "@!@!@!@{Option4} "
                 + "==========!!\n"
                 }
                ]

    response = client.chat.completions.create(model=model, messages=messages) #우선 json형태로 반환받아보기
    answer = response.choices[0].message.content

    print(answer)

    divided_problems = answer.split("==========!!") #문제, Option 기준으로 나누기

    print(divided_problems)

    problem_list = [] #'문제', '옵션' / '문제', '옵션' /.... 이런식으로 저장됨. 단 옵션은 없으면 None으로 처리

    problem_counter = 0
    while problem_counter < len(divided_problems) - 1:  # 마지막 분할은 비어있을 수 있으므로 제외
        question = divided_problems[problem_counter].strip() + '?'
        problem_counter += 1  # 옵션으로 이동
        
        # 옵션 처리: 공백으로 구분된 옵션들을 배열로 변환
        options_str = divided_problems[problem_counter].strip()
        if options_str:
            options = [option.strip() for option in options_str.split("@!@!@!@") if option.strip()]
        else:
            options = None
        problem_counter += 1  # 다음 문제로 이동

        print(options)

        # 문제 객체 생성 및 리스트에 추가
        db_problem = problem_crud.create_problem(db, quiz_id=quiz_id, question=question, options=options or [], difficulty=db_quiz.difficulty)
        problem_list.append(db_problem)

    return problem_list #Problem을 List형식으로 반환



@router.post("/{quiz_id}") #우선 모든 질문에 모두 답하는 것으로 함.
async def Check_User_Answer(problems: List[problem_schema.problem], quiz_id :int, user_answer: str):

    history = ""

    count = 1
    print(problems)
    for problem in problems:
        print(problem)
        history += f"{problem.question}\n"
        print(history)
        if problem.options:
            print(problem.options)
            options_str = "\n".join([f"{i+1}: {option}" for i, option in enumerate(problem.options)])
            print(options_str)
            history += f"{options_str}\n\n"
        else:
            history += "선택지 없음\n\n"
        count = count +1

    print("we are out\n")
    model = MODEL

    print(history)

    query = f"Please verify {user_answer} is correct, as the Answer of Question : \n{history} ."

    messages = [{"role": "system", "content" : "Check the before you maded question and verify user answers.\n If user answer is correct, please say in korean."},
                {"role": "user", "content" : query},
                {"role": "assistant", "content" : "Please verify the answer of input question is Correct or False.\n And then Teach me what real answer is and why it is. \n"
                 +  "If user answer is 'user_answer1, user_answer2', The first question of user answer is 'user_answer1' and the next question of user answer is 'user_answer2'.  \n"
                 + "The output format should be as follows. \n"
                 + "Format:"
                 + "{question} ==========!!"
                 + "{user_answer1} ==========!! {gpt_answer_option_number} ==========!!"
                 + "{gpt_exaplanation_reason}@@==========@@"
                 + "{question}==========!!"
                 + "{user_answer2}==========!!{gpt_answer_option_number}==========!!"
                 + "{gpt_exaplanation_reason}@@==========@@"
                 }]
    
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content

    sets = answer.strip().split("@@==========@@")
    final_dict = {}

    print ("before loop")

    # 각 세트를 순회하며 처리
    for i, set in enumerate(sets, start=1):
        if set:  # 세트가 비어있지 않은 경우에만 처리
            parts = set.strip().split("==========!!")
            # 세부 항목 분리 및 딕셔너리 구성
            question = parts[0].strip()
            user_answer = parts[1].strip()
            gpt_answer = parts[2].strip()
            reason = parts[3].strip()

            # 최종 딕셔너리에 추가
            final_dict[i] = {
                "question": question,
                "user_answer": user_answer,
                "gpt_answer": gpt_answer,
                "reason": reason
            }

    # 결과 출력
    print(final_dict)

    print("ended\n")

    return final_dict