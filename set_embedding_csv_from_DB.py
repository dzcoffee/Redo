
import pandas as pd
import os

from database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.logger import logger

from domain.problem import problem_schema, problem_crud

OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"
from openai import OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)



problem_list = []

problem_id_list = [179,180,181,182]

db:Session = next(get_db())

file_path = "problem_csv/인공지능_problems.csv"

for problem_id in problem_id_list:
    problem = problem_crud.get_problem(db, problem_id)
    if problem:
        gpt_embeddings_input = problem.question + "\n 1)" + problem.options[0] + "\n 2)" + problem.options[1] + "\n 3)" + problem.options[2] + "\n 4)" + problem.options[3]
        res = client.embeddings.create(
                input = gpt_embeddings_input,
                model = 'text-embedding-3-large'
            )
        embedding = res.data[0].embedding

        problem_list.append({
            'id' : problem.id,
            'embeddings' : embedding
        })


# 데이터프레임 생성
df = pd.DataFrame(problem_list)

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