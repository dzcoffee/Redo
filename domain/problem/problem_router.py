from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import get_db

from sqlalchemy.orm import Session

from typing import List, Optional

from openai import OpenAI



OPENAI_API_KEY = "sk-proj-ICgDke4pZhfQGVjRbLXVT3BlbkFJCXouIJ1ARFKa6EPFZ0M9"

client = OpenAI(
    api_key = OPENAI_API_KEY
)

MODEL = "gpt-4-turbo" #json형식 return 받으려면 1106버전 이상 

DB_Problem_List = []

router = APIRouter(
    prefix="/quiz/game",
)
###임시 추가 Pydantic 모델 코드
class Problem(BaseModel):
    id : int
    quizid : int
    question : str
    answer : Optional[str] = None
    difficulty : str

class Quiz(BaseModel):
    id : int
    writer : int
    type : str
    count : int
    difficulty : str

class QM_link(BaseModel):
    id : int
    quizid : int
    memoid : int

class Memo(BaseModel):
    id : int
    content : str

##### 추가로 작성해야 하는 API
##### 1. /quiz에서 memo DB의 title이랑 id 값 불러와서 get 형식으로 보내주기
##### 2. /quiz 에서 quiz option 받아오는 post형식 api -> DB에 저장 및 problems로 갈 때 quiz_id 넘겨주기
##### 3. /문제 만들어진거 대답 넣어서 오답 확인하는 post 형식 api


#선택한 옵션으로 gpt api를 통해 생성된 문제를 쏴주는 api
@router.get("", response_model=List[Problem]) # << Problem entity Pydantic모델의 리스트로 리턴받음. ##, response_model=List[Problem]## 추가할 것
async def Create_problems(quiz_id: int):
    
    ##quiz_id로 quiz 정보 db에 요청
    ##db에서 값을 받아왔다고 가정(CRUD)
    db_quiz = Quiz(id = 44, writer = 234, type = "객관식", count = 2, difficulty = "쉬움")

    ##quiz_id로 묶인 memo 정보 db에 요청해서 가져왔다고 가정(CRUD)
    db_qmLink = QM_link(id=1, quizid=44, memoid=234)

    ##memo_id를 이용해 db에서 memo 정보 가져옴 가정(CRUD)
    db_memo = Memo(id = 234, content = "Clustered System - 높은 범용성 (대칭성, 비대칭성 있음) - 병렬을 사용하여 높은 퍼포먼스 컴퓨팅을 가진다(HPC ; High Performance Computing) - 각각의 충돌을 방지하기 위해 DLM(distributed lock manager)을 가짐- 네트워크를 통해 저장장치를 공유한다. SAN(Storage-Area Network)") 

    model = MODEL 

    query = f"{db_memo.content}라는 내용을 바탕으로 {db_quiz.type}형태로, {db_quiz.count}개의 문제를 만들어줄래?" #json 형태 반환 시 json이 query에 포함되어 있어야함
    #difficulty는 일단 제외 테스트 후 추가

    messages = [{"role": "system","content": "You are a helpful quiz maker system and also verify user answers and speak Korean "}, 
                {"role": "user","content": query},
                {"role": "system", "content" : "The output format should be as follows'. The number of quesiton follow in the user input. You must not say 'any other things' before '1.'. Also you must input Separtor '==========!!' between Qusetion and Option and also each 'Question set(Qusertions+Option)'\n"
                 +"Format:\n"
                 +"{number of question}. {Question}"
                 #+"==========!!"
                 + "1){Option1} "
                 + "2){Option2} "
                 + "3){Option3} "
                 + "4){Option4} "
                 +"==========!!"
                 + "{next number of question}. {Question}"
                 #+"==========!!"
                 + "1){Option1} "
                 + "2){Option2} "
                 + "3){Option3} "
                 + "4){Option4} "
                 + "The Example of format is as follows.\n"
                 + " 1. Something you made question"
                 + " 1) Answer_1 2) Answer_2 3) Answer_3 4) Answer_4==========!!"
                 + " 2. Something you made question"
                 + " 1) Answer_1 2) Answer_2 3) Answer_3 4) Answer_4==========!!"
                 }
                ]

    response = client.chat.completions.create(model=model, messages=messages) #우선 json형태로 반환받아보기
    answer = response.choices[0].message.content

    print(answer)

    divided_problems = answer.split("==========!!") #문제, Option 기준으로 나누기

    print(divided_problems)

    problem_list = [] #'문제 + 옵션' / '문제 + 옵션' /.... 이런식으로 저장됨.

    problem_counter = 0
    while problem_counter < db_quiz.count: #문제 갯수에 맞게 배열에 저장
        db_problem = Problem(id=problem_counter+1, quizid= db_quiz.id, question=divided_problems[problem_counter], difficulty=db_quiz.difficulty)
        problem_list.append(db_problem)
        problem_counter = problem_counter+1  #문제, 옵션 이런식이니 2단계 넘어야 함.


    DB_Problem_List = problem_list #DB에 저장했다고 가정

    print(DB_Problem_List)

    return problem_list #Problem을 List형식으로 반환



@router.post("/{problem_id}")
async def Check_User_Answer(problems: List[Problem], check_problem_id :int, user_answer: str):

    history = None
    for problem in problems:
        if problem.id == check_problem_id:
            history = problem.question
            break

    model = MODEL

    query = f"The Answer of Question '{history}' is '{user_answer}'."

    messages = [{"role": "system", "content" : f"Check the question '{history}' and verify user answers. If user answer is correct, please say in korean."},
                {"role": "user", "content" : query},
                {"role": "assistant", "content" : "Please verify the answer of input question is Correct or False. And then Teach me what real answer is and why it is."}]
    
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content

    print(answer)

    return answer