import openai
from fastapi import APIRouter, Depends, HTTPException

from openai import OpenAI

from database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

import json

from auth.auth_validator import AuthValidator
from domain.memo import memo_schema, memo_crud
from domain.quiz import quiz_schema, quiz_crud
from domain.quiz_memo_group import memoQuizGroup_schema, memoQuizGroup_crud
from domain.problem import problem_schema, problem_crud

from pydantic import BaseModel


OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"

client = OpenAI(
    api_key = OPENAI_API_KEY
)


MODEL = "gpt-4o" #json형식 return 받으려면 1106버전 이상 


DB_Problem_List = []

router = APIRouter(
    prefix="/quiz/game",
    dependencies=[Depends(AuthValidator())]
)

async def moderate_text(text: str):
    response = openai.Moderation.create(input=text)
    return response['results'][0]

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

    query = f" '''{db_memo.content}'''라는 내용을 바탕으로 '{db_quiz.type}'형태로, {db_quiz.count}개의 문제를 만들어줄래?" #이것도 토큰 수 절약할 꺼면 영어로 번역하면 됨.
    #difficulty는 일단 제외 테스트 후 추가

    messages = [{"role": "system","content": "You are a helpful quiz maker system and also speak Korean "}, 

                {"role": "user","content": query},
                {"role": "system", "content" : "The output format should be as follows, but If type is not '객관식', Please answer without option like '@@!!!!!!@@{Option1}', '@@!!!!!!@@{Option2}'.\n The number of quesiton follow the user input, but do not put 'the number' before question, just answer Question string.\n You must not say 'any other things' before 'Question'.\n Also you must input Separtor.\n Answer must be correct Answer.\n Commentary must be explaining how can you find the answer.\n Don't put 'Colon' Before any { } instance. '\n"
                 +"Format:\n"
                 +"{Question}?"
                 +"##==========!!"
                 + "@@!!!!!!@@{Option1} "
                 + "@@!!!!!!@@{Option2} "
                 + "@@!!!!!!@@{Option3} "
                 + "@@!!!!!!@@{Option4} "
                 +"##==========!!"
                 +"{Answer}"
                 +"##==========!!"
                 +"{Commentary}"
                 +"##==========!!"
                 + "{Question}?"
                 +"##==========!!"
                 + "@@!!!!!!@@{Option1} "
                 + "@@!!!!!!@@{Option2} "
                 + "@@!!!!!!@@{Option3} "
                 + "@@!!!!!!@@{Option4} "
                 + "##==========!!"
                 +"{Answer}"
                 +"##==========!!"
                 +"{Commentary}"
                 +"##==========!!"
                 }
                ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0.8, max_tokens=2048) #temperature 0.8이 한국어에 가장 적합하다는 정보가 있어서 적용시켜봄.
    answer = response.choices[0].message.content #GPT의 답변 받는 거임.

    print(answer)

    divided_problems = answer.split("##==========!!") #문제, Option, Answer, commentary 기준으로 나누기

    print(divided_problems)

    problem_list = [] #'문제', '옵션' / '문제', '옵션' /.... 이런식으로 저장됨. 단 옵션은 없으면 None으로 처리

    problem_counter = 0
    while problem_counter < len(divided_problems) - 1:  # 마지막 분할은 비어있을 수 있으므로 제외
        question = divided_problems[problem_counter].strip() + '?'
        problem_counter += 1  # 옵션으로 이동

        
        if db_quiz.type == "객관식":

            options = None
        else:
            # 옵션 처리: 공백으로 구분된 옵션들을 배열로 변환
            options_str = divided_problems[problem_counter].strip()
            if options_str:
                options = [option.strip() for option in options_str.split("@@!!!!!!@@") if option.strip()]
            else:
                options = None
        problem_counter += 1  # 다음 문제로 이동

        print(options) 

        Quiz_ans = divided_problems[problem_counter].strip()
        problem_counter += 1

        print(Quiz_ans)

        Quiz_commentary  = divided_problems[problem_counter].strip()
        problem_counter += 1

        print(Quiz_commentary)

        # 문제 객체 생성 및 리스트에 추가
        db_problem = problem_crud.create_problem(db, quiz_id=quiz_id, question=question, options=options or [], difficulty=db_quiz.difficulty, answer = Quiz_ans, comentary= Quiz_commentary)
        problem_list.append(db_problem)

    return problem_list #Problem을 List형식으로 반환



@router.post("/{quiz_id}") #우선 모든 질문에 모두 답하는 것으로 함.
async def Check_User_Answer(problems: List[problem_schema.problem], quiz_id :int, user_answer: List[str]):

    history = ""
    type = 0 # 0 : 단답, 주관식 , 1: 객관식


    final_dict = {} #반환하는 dict 형 변수

    if problems[0].options: #첫 문제로 단답, 객관식 판별(option있으면 객관식)
        type = 1
    
    problem_count = 0
    if(type == 1):
        print("객관식임\n")
        for problem in problems:
            check_answer = user_answer[problem_count] #N번째 문제의 유저 답변 
            check_answer = int(check_answer) - 1  # str형 -> int형, 1번부터 ~ -> 0번부터 ~
            User_TF = "False"
            print(check_answer)
            print(problem.answer)
            print(problem.options[check_answer])
            if problem.options[check_answer] == problem.answer: #해당 선지 번호의 답변과 problem.answer가 동일하다면 True
                User_TF = "True"
            
            final_dict[problem_count] = {
                "question": problem.question,
                "user_answer": check_answer,
                "gpt_answer": problem.answer,
                "gpt_TF" : User_TF,
                "reason": problem.comentary

            }
            problem_count = problem_count +1

             # 결과 출력
            print(final_dict)
            

    if(type == 0):
        print("주관식임\n")
        count = 1
        print(problems)
        for problem in problems: 
            history += f"Question {count} : {problem.question}\n"

            ## 원래 객관식 option 처리해주던 거
            # if problem.options:
            #     print(problem.options)
            #     options_str = "\n".join([f"{i+1}: {option}" for i, option in enumerate(problem.options)])
            #     print(options_str)
            #     history += f"{options_str}\n\n"
            # else:
            #     history += "선택지 없음\n\n"
            count = count +1

        print("we are out\n")
        model = MODEL


        query = f"Please verify {user_answer} is correct, as the Answer of Question : {history} ."

        messages = [{"role": "system", "content" : "Check the before you maded question and verify user answers.\n"},
                    {"role": "user", "content" : query},
                    {"role": "assistant", "content" : "Please verify the answer of input question is Correct or False.\n And then Teach me what real answer is and why it is. \n"
                    +  "If there are Options and user answer is ['A1', 'A2'], The Question 1 of user answer is 'A1' and the Question 2 of user answer is 'A2'.  \n"
                    + "{gpt_answer} is Only A Answer that you verifed by question, '''Do not contain a Question.'''  \n"
                    + "{gpt_Ture_False} form must be 'True' or 'False'.\n"
                    + "{gpt_exaplanation_reason} is 'the reason' user answer is True or False.\n"
                    + "And each Set(gpt_answer, gpt_True_False, gpt_answer) must allocated at A Question and Each Set is divided by seperator '@@==========@@'.\n"
                    + "Please do not answer with any 'Colon', Attribute like 'gpt_answer:' and bracket."
                    + "The output format must be as follows with korean.\n"
                    + "Format:"
                    + "{gpt_answer}==========!!{gpt_Ture_False}==========!!"
                    + "{gpt_exaplanation_reason}@@==========@@"
                    + "{gpt_answer}==========!!{gpt_Ture_False}==========!!"
                    + "{gpt_exaplanation_reason}@@==========@@"
                    }]
        
        
        response = client.chat.completions.create(model=model, messages=messages)
        answer = response.choices[0].message.content

        print(answer)

        print("\n\nit is answer \n\n ")

        sets = answer.strip().split("@@==========@@")

        #moderation 적용
        for set in sets:
            moderation_result = await moderate_text(set)
            if moderation_result["flagged"]:
                # 모데레이션에서 부적절한 콘텐츠 감지
                return {"error": "Inappropriate content detected in the response"}

        print (sets)

        print("\nthis is user answer : \n")
        print(user_answer)

        # 각 세트를 순회하며 처리
        count_num = 0 #아래 problems와 user_answer 체크용 변수
        for i, set in enumerate(sets, start=1):
            if set:  # 세트가 비어있지 않은 경우에만 처리
                parts = set.strip().split("==========!!")
                # 세부 항목 분리 및 딕셔너리 구성
                question = problems[count_num].question
                answer_by_user = user_answer[count_num]
                gpt_answer = parts[0].strip()
                gpt_TF = parts[1].strip()
                reason = parts[2].strip()

                # 최종 딕셔너리에 추가
                final_dict[i] = {
                    "question": question,
                    "user_answer": answer_by_user,
                    "gpt_answer": gpt_answer,
                    "gpt_TF" : gpt_TF,
                    "reason": reason
                }
                count_num = count_num+1

        # 결과 출력
        print(final_dict)

       

        print("ended\n")

    return final_dict



@router.post("/{quiz_id}/feedBack", response_model=Optional[problem_schema.problem])
async def FeedBack(quiz_id: int, problem_id: int, feedback: int, db: Session = Depends(get_db)):
    if feedback < 1 or feedback > 10:
        raise HTTPException(status_code=400, detail="Feedback must be between 1 and 10")

    #문제 가져오기
    db_problem = problem_crud.get_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    if feedback <= 4:
        if problem_crud.delete_problem_if_low_feedback(db, problem_id, feedback):
            return feedback

    # 문제에 피드백 저장
    db_problem.feedback = feedback
    db.commit()
    db.refresh(db_problem)

