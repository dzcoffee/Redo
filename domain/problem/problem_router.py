from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from openai import OpenAI


import pandas as pd
import os

from database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.logger import logger


import random as rnd


from auth.auth import user_from_request

from numpy import dot
from numpy.linalg import norm
import numpy as np

from auth.auth_validator import AuthValidator
from domain.memo import memo_schema, memo_crud
from domain.quiz import quiz_schema, quiz_crud
from domain.quiz_memo_group import memoQuizGroup_schema, memoQuizGroup_crud
from domain.problem import problem_schema, problem_crud

from pydantic import BaseModel, ValidationError


OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"


client = OpenAI(
    api_key=OPENAI_API_KEY
)

MODEL = "gpt-4o" #json형식 return 받으려면 1106버전 이상 


DB_Problem_List = []

router = APIRouter(
    prefix="/quiz/game",
    dependencies=[Depends(AuthValidator())],
    tags=["문제"]
)

def moderate_text(text: str):
    response = client.moderations.create(input=text)
    return response.results[0]

#선택한 옵션으로 gpt api를 통해 생성된 문제를 쏴주는 api
@router.get("/{quiz_id}", response_model=List[problem_schema.problem]) # << Problem entity Pydantic모델의 리스트로 리턴받음. ##, response_model=List[Problem]## 추가할 것
async def Create_problems(quiz_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = user_from_request(request)
    ##quiz_id로 quiz 정보 db에 요청
    db_quiz = quiz_crud.get_quiz_id(db, quiz_id)

    ##quiz_id로 묶인 memo 정보 db에 요청
    db_memo= memoQuizGroup_crud.get_memoId(db, quiz_id) ## 이거 내부 코드 수정을 해야됨.

    if db_memo is None:
    # 적절한 예외 처리나 오류 메시지 반환
        raise HTTPException(status_code=404, detail="Memo not found")
    
    
    df = pd.read_csv(f'memo_csv/{user_id}_memo.csv')
    result_row = df[df.iloc[:, 0] == db_memo.id]

    logger.info(result_row)

    if not result_row.empty:
        memo_embeddings = result_row.iloc[0, 1]
        #print(f"메모 임베딩값: {memo_embeddings}\n")
    else:
        print("해당 memo_id 값을 찾을 수 없습니다.")
    

    if(db_quiz.count == 1):
        gpt_quiz_count = 1
    else:
        gpt_quiz_count = rnd.randint(round(db_quiz.count/2), db_quiz.count-1) # GPT 문제 생성 갯수(랜덤)

    embeddings_quiz_count = db_quiz.count - gpt_quiz_count #만들기로 한 갯수 중 gpt 문제 생성 갯수 제외한 임베딩 문제 갯수
    embeddings_quiz_count_final = 0
    if(embeddings_quiz_count != 0):
        embedded_problem = get_problems_from_embeddings(embeddings_quiz_count, memo_embeddings, db_memo.categories)
        embeddings_quiz_count_final = len(embedded_problem)
        if embedded_problem == None:
            gpt_quiz_count = db_quiz.count #만약 해당 카테고리의 csv파일 없으면 원래대로 gpt한테 전부 생성 요청
        

        logger.info(embeddings_quiz_count_final)

    embedded_problem_list = []
    print("임베디드프라블럼 추가 전")
    added_embedded_problem_count = 0
    logger.info(embedded_problem_list)
    if(embeddings_quiz_count_final!=0): #만약 가져온 문제 id가 있으면
        for db_problem_id in embedded_problem:
            if added_embedded_problem_count == embeddings_quiz_count:
                break
            db_problem_id = int(db_problem_id)
            logger.info(db_problem_id)
            saved_problem = problem_crud.get_problem(db, db_problem_id)
            saved_problem.correctness = 101 # 101 : 임베딩 DB문제 코드
            if(db_quiz.type == "객관식"): #객관식에 맞는 option이 있는 문제인 경우 가져오기
                if(saved_problem.options):
                    logger.info(saved_problem)
                    embedded_problem_list.append(saved_problem)
                    added_embedded_problem_count += 1
            else: #
                if(saved_problem.options == []):
                    logger.info(saved_problem)
                    embedded_problem_list.append(saved_problem)
                    added_embedded_problem_count += 1
                else:
                    continue
        gpt_quiz_count = db_quiz.count - added_embedded_problem_count
            
    difficulty = db_quiz.difficulty
    if difficulty == '쉬움':
        persona = "You are a high school student with a basic understanding of programming concepts and algorithms."
        include_code_sample = False
    elif difficulty == '중간':
        persona = "You are a college student majoring in computer science."
        include_code_sample = False
    elif difficulty == '어려움':
        persona = "You are a job seeker preparing for technical interviews in the field of software development. "
        include_code_sample = True


    print(f"gpt 문제 만드는 갯수는 : {gpt_quiz_count}, 임베딩 문제 가져오는 갯수 : {added_embedded_problem_count}\n")

    model = MODEL

    if db_quiz.type == "객관식":
        problem_type = "multiple choice"   
    elif db_quiz.type == "단답식":
        problem_type = "short answer"    
    elif db_quiz.type == "주관식":
        problem_type = "essay question"
        
    


    #query = f" '''{db_memo.content}'''라는 내용을 바탕으로 ''{problem_type}''형태로, {gpt_quiz_count}개의 문제를 만들어줄래? 문제의 수준은 '{persona}'에 맞게 만들어줘." #이것도 토큰 수 절약할 꺼면 영어로 번역하면 됨.
    #difficulty는 일단 제외 테스트 후 추가

    query = f"Could you create {gpt_quiz_count} problems in the form of '{problem_type}' based on the content '''{db_memo.content}'''? Please make sure the difficulty level is suitable for user persona like '{persona}'."

    if include_code_sample:
        query += "Please include a code sample or table in the {Question} field !!! "
    else:
        query += "Please Don't include a code sample or table in the {Question} field !!! "
    
    system_message = ""
    
    if db_quiz.type == "객관식":
        system_message_1 = """
        The output format should be as follows.  
        Don't forget field separator '##==========##' after {Question}. 
        Don't input 'line break' and 'spacing' between separator.  
        The number of quesiton follow the user input, but do not put 'the number' and string '{Question}' before question, just answer Question string.
        You must not say 'any other things' before Question.
        Answer must be correct Answer.
        Commentary must be explaining how can you find the answer.
        Don't put 'Colon' Before any instance.
        Don't forget separator '##==========##' between each Quiz(with fields).

        Format:\n
        {Question}?
        ##==========##
        @@!!!!!!@@{Option1}
        @@!!!!!!@@{Option2}
        @@!!!!!!@@{Option3}
        @@!!!!!!@@{Option4}
        ##==========##
        {Answer}
        ##==========##
        {Commentary}
        ##==========##
        {Question}?
        ##==========##
        @@!!!!!!@@{Option1}
        @@!!!!!!@@{Option2}
        @@!!!!!!@@{Option3}
        @@!!!!!!@@{Option4}
        ##==========##
        {Answer}
        ##==========##
        {Commentary}
        ##==========##
        """
        system_message = system_message_1
    else:
        system_message_2 = """
        The output format should be as follows.  
        Don't forget field separator '##==========##' after {Question}. 
        Don't input 'line break' and 'spacing' between separator.  
        The number of quesiton follow the user input, but do not put 'the number' and string '{Question}' before question, just answer Question string.
        You must not say 'any other things' before Question.
        Answer must be correct Answer.
        Commentary must be explaining how can you find the answer.
        Don't put 'Colon' Before any instance.
        Don't forget separator '##==========##' between each Quiz(with fields) it means after {Commentary}!!.
        
        Format:\n
        {Question}?
        ##==========##
        {Answer}
        ##==========##
        {Commentary}
        ##==========##
        {Question}?
        ##==========##
        {Answer}
        ##==========##
        {Commentary}
        ##==========##
        """
        system_message = system_message_2

    #print(system_message_1)

    messages = [{"role": "system","content": f"You are a helpful quiz maker system and also speak Korean. if "}, 
                {"role": "user","content": query},
                {"role": "system", "content" : system_message
                 }
                ]

    response = client.chat.completions.create(model=model, messages=messages) #temperature 0.8이 한국어에 가장 적합하다는 정보가 있어서 적용시켜봄.
    answer = response.choices[0].message.content #GPT의 답변 받는 거임.

    logger.info(answer)

    divided_problems = answer.split("##==========##") #문제, Option, Answer, commentary 기준으로 나누기

    logger.info(divided_problems)

    problem_list = [] #'문제', '옵션' / '문제', '옵션' /.... 이런식으로 저장됨. 단 옵션은 없으면 None으로 처리

    problem_counter = 0
    while problem_counter < len(divided_problems) - 1:  # 마지막 분할은 비어있을 수 있으므로 제외
        question = divided_problems[problem_counter].strip()
        problem_counter += 1  # 옵션으로 이동

        if db_quiz.type != "객관식":
            options = None
        else:
            # 옵션 처리: 공백으로 구분된 옵션들을 배열로 변환
            options_str = divided_problems[problem_counter].strip()
            if options_str:
                options = [option.strip() for option in options_str.split("@@!!!!!!@@") if option.strip()]
            else:
                options = None
            problem_counter += 1  # 다음 문제로 이동

        logger.info(quiz_id)
        logger.info(question)
        logger.info(db_quiz.difficulty)
        logger.info(options) 

        Quiz_ans = divided_problems[problem_counter].strip()
        problem_counter += 1

        logger.info(Quiz_ans)

        Quiz_commentary  = divided_problems[problem_counter].strip()
        problem_counter += 1

        logger.info(Quiz_commentary)

        # 문제 객체 생성 및 리스트에 추가
        db_problem = problem_crud.create_problem(db, quiz_id=quiz_id, question=question, options=options or [], difficulty=db_quiz.difficulty, answer = Quiz_ans, comentary= Quiz_commentary)
        
        if db_quiz.type == '객관식':
            gpt_embeddings_input = db_problem.question + "\n 1)" + db_problem.options[0] + "\n 2)" + db_problem.options[1] + "\n 3)" + db_problem.options[2] + "\n 4)" + db_problem.options[3]
        else :
            gpt_embeddings_input = db_problem.question
    
        logger.info(gpt_embeddings_input)

        res = client.embeddings.create(
            input = gpt_embeddings_input,
            model = 'text-embedding-3-large'
        )

        gpt_Make_embedding = res.data[0].embedding #gpt한테서 막 나온 embedding
       # print(gpt_Make_embedding)

        gpt_Make_embedding_string= ','.join(map(str, gpt_Make_embedding)) # gpt 생성 문제 embedding 문자열화
        memo_embeddings_string = np.fromstring(memo_embeddings[1:-1], sep=',')
        gpt_Make_embedding_array = np.fromstring(gpt_Make_embedding_string[1:-1], sep=',')

        MP_similarities = cos_sim(memo_embeddings_string, gpt_Make_embedding_array)
        print("유사도\n")
        logger.info(MP_similarities)

        PP_similarities = similarities_Problem_in_embbeding_DB(gpt_Make_embedding_string, db_memo.categories)

        Top_similaritiy = Top_similarities_Problem_in_embbeding_DB(gpt_Make_embedding_string, db_memo.categories)

        correctness = int((MP_similarities + PP_similarities)*100/2)
        logger.info(correctness)
        db_problem.correctness = correctness

        problem_list.append(db_problem)
        logger.info(db_problem)

        if(Top_similaritiy*100 <= 80):
            path = f'problem_csv/{db_memo.categories}_problems.csv'
            data_list = []
            data_list.append({
                'id' : db_problem.id,
                'embeddings' : gpt_Make_embedding
            })
            csv_save(path, data_list)


    problem_list.extend(embedded_problem_list)

    print("프라블럼 리스트 함수 나오기 전")
    print(problem_list)

    #problem_list.append(embedded_problem)
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
        logger.info("객관식임\n")
        for problem in problems:
            check_answer = user_answer[problem_count] #N번째 문제의 유저 답변 
            check_answer = int(check_answer) - 1  # str형 -> int형, 1번부터 ~ -> 0번부터 ~
            User_TF = "False"
            logger.info(check_answer)
            logger.info(problem.answer)
            logger.info(problem.options[check_answer])
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
            logger.info(final_dict)
            

    if(type == 0):
        logger.info("주관식임\n")
        count = 1
        logger.info(problems)
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

        logger.info("we are out\n")
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

        logger.info(answer)

        logger.info("\n\nit is answer \n\n ")

        sets = answer.strip().split("@@==========@@")

        #moderation 적용
        for set in sets:
            moderation_result = moderate_text(set)
            if moderation_result.flagged:
                # 모데레이션에서 부적절한 콘텐츠 감지
                return {"error": "Inappropriate content detected in the response"}

        logger.info(sets)

        logger.info("\nthis is user answer : \n")
        logger.info(user_answer)

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
        logger.info(final_dict)

       

        logger.info("ended\n")

    return final_dict


@router.get("/problems/check", response_model=List[problem_schema.problem])
async def get_problem_api(problem_id: int, request: Request, db: Session = Depends(get_db)):
    embedded_problem = problem_crud.get_problem(db, problem_id)
    list_problem = [embedded_problem]
    return list_problem


@router.post("/{quiz_id}/feedBack", response_model=Optional[problem_schema.problem])
async def FeedBack(quiz_id: int, problem_id: int, feedback: int, db: Session = Depends(get_db)):
    ##quiz_id로 묶인 memo 정보 db에 요청
    db_memo= memoQuizGroup_crud.get_memoId(db, quiz_id)
    file_path = f'problem_csv/{db_memo.categories}_problems.csv'
    df = pd.read_csv(file_path)
    # 첫 번째 열 이름 가져오기
    first_col_name = df.columns[0]

    if feedback < 1 or feedback > 10:
        raise HTTPException(status_code=400, detail="Feedback must be between 1 and 10")

    #문제 가져오기
    db_problem = problem_crud.get_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    if feedback <= 7:
        if problem_crud.delete_problem_if_low_feedback(db, problem_id, feedback):
            # problem_id와 동일한 값이 있는 행 삭제
            # problem_id와 동일한 값이 있는지 확인
            if problem_id not in df[first_col_name].values:
                raise ValueError(f"problem_id '{problem_id}' not found in the first column.")
            
            # problem_id와 동일한 값이 있는 행 삭제
            df = df[df[first_col_name] != problem_id]
        
            # 수정된 DataFrame을 CSV 파일로 저장
            df.to_csv(file_path, index=False)
            return feedback

    # 문제에 피드백 저장
    db_problem.feedback = feedback
    db.commit()
    db.refresh(db_problem)


# 코사인 유사도 계산 함수
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))


def get_problems_from_embeddings(embeddings_quiz_count, memo_embeddings, category):
        try:
            df = pd.read_csv(f'problem_csv/{category}_problems.csv')
        except:
            return None

        problem_embeddings = df.iloc[:,1].tolist()
        problem_embeddings = [np.fromstring(x[1:-1], sep=',') for x in problem_embeddings] # 문자열을 numpy 배열로 변환

        memo_embeddings = np.fromstring(memo_embeddings[1:-1], sep=',')
        
        # 코사인 유사도 계산
        similarities = [cos_sim(memo_embeddings, pe) for pe in problem_embeddings]

        # 유사도와 인덱스를 함께 유지하며 0.5 이상인 유사도 필터링(0.5이상은 유사한 것으로 판단)
        filtered_similarities = [(i, sim) for i, sim in enumerate(similarities) if sim < 0.5 and sim > 0.3]

        logger.info(filtered_similarities)

        # 유사도가 높은 순으로 정렬하고 상위 embeddings_quiz_count개 선택
        filtered_similarities.sort(key=lambda x: x[1], reverse=True)
        num_problems_to_select = min(20, len(filtered_similarities))
        
        top_indices = [filtered_similarities[i][0] for i in range(num_problems_to_select)]
        top_problem_id = [df.iloc[i, 0] for i in top_indices]

        return top_problem_id


def similarities_Problem_in_embbeding_DB(memo_embeddings, category):
        try:
            df = pd.read_csv(f'problem_csv/{category}_problems.csv')
        except:
            return None
        
        problem_embeddings = df.iloc[:,1].tolist()
        problem_embeddings = [np.fromstring(x[1:-1], sep=',') for x in problem_embeddings] # 문자열을 numpy 배열로 변환

        memo_embeddings = np.fromstring(memo_embeddings[1:-1], sep=',')

        # 코사인 유사도 계산
        similarities = [cos_sim(memo_embeddings, pe) for pe in problem_embeddings]

        average_similarity = np.mean(similarities)

        print(f"임베딩 DB와 평균 유사도는 : {average_similarity}%입니다.")

        return average_similarity


def Top_similarities_Problem_in_embbeding_DB(memo_embeddings, category):
        try:
            df = pd.read_csv(f'problem_csv/{category}_problems.csv')
        except:
            return None

        problem_embeddings = df.iloc[:,1].tolist()
        problem_embeddings = [np.fromstring(x[1:-1], sep=',') for x in problem_embeddings] # 문자열을 numpy 배열로 변환

        memo_embeddings = np.fromstring(memo_embeddings[1:-1], sep=',')

        # 코사인 유사도 계산
        similarities = [cos_sim(memo_embeddings, pe) for pe in problem_embeddings]

        high_similarity = max(similarities)

        print(f"임베딩 DB와 가장 높은 유사도는 : {high_similarity}%입니다.")

        return high_similarity

def csv_save(file_path, data_list):
    # 데이터프레임 생성
    df = pd.DataFrame(data_list)

    #print(data_list)
    # 파일이 존재하는지 확인
    if os.path.exists(file_path):
        # 파일이 존재하면 기존 데이터를 읽어옵니다.
        existing_df = pd.read_csv(file_path)
        # 새로운 데이터프레임을 기존 데이터에 추가합니다.
        df = pd.concat([existing_df, df], ignore_index=True)
    else:
        print(f"{file_path} 파일이 존재하지 않으므로 새로 생성합니다.")

    # 데이터프레임을 CSV 파일에 저장
    df.to_csv(file_path, index=False)

    print(f"데이터가 {file_path}에 저장되었습니다.")