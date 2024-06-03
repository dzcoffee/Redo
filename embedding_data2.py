from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

import openai

import pandas as pd
import os

file_path = "./problems.csv"

openai.api_key = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"
model = 'text-embedding-3-small'

driver = webdriver.Chrome()

check_count = 1
while(check_count <= 74):
    driver.get("https://www.tutorialspoint.com/questions_and_answers.htm")
    driver.implicitly_wait(2)

    tutorial_page = driver.find_element(by=By.XPATH, value=f"/html/body/section/div/div/div[4]/ul/li[{check_count}]/a")
    tutorial_title = tutorial_page.get_attribute("title")
    
    if tutorial_title.startswith("SAP"): #SAP로 시작하는 요소들 모두 생략
        check_count+=1
        print(f"이 퀴즈는 SAP 요소 이므로 생략합니다. title : {tutorial_title}")
        continue
    
    tutorial_page.click()
    driver.implicitly_wait(2)

    data_list = []

    check_test_count = 1
    while(check_test_count <= 4):
        next_tutorial_page = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/a[{check_test_count}]/button")
        next_tutorial_page.click()
        driver.implicitly_wait(2)

        number_of_Problems = 5
        while(number_of_Problems <= 28):
            question = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/div[{number_of_Problems}]/div[1]/p[1]").text
            option1_before = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/div[{number_of_Problems}]/div[1]/p[2]/a").text
            option1 = option1_before.split(' - ')[1]

            option2_before = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/div[{number_of_Problems}]/div[1]/p[3]/a").text
            option2 = option2_before.split(' - ')[1]

            option3_before = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/div[{number_of_Problems}]/div[1]/p[4]/a").text
            option3 = option3_before.split(' - ')[1]

            option4_before = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/div[{number_of_Problems}]/div[1]/p[4]/a").text
            option4 = option4_before.split(' - ')[1]

            answer = driver.find_element(by=By.XPATH, value=f"/html/body/main/div/div/div[2]/table/tbody/tr[{number_of_Problems-3}]/td[2]").text

            gpt_embeddings_input = question + '\n1)' + option1 + '\n2)' + option2 + '\n3)' + option3 + '\n4)' + option4

            res = openai.embeddings.create(
                input = gpt_embeddings_input,
                model = 'text-embedding-3-small'
            )

            embedding = res.data[0].embedding

            print(embedding)

            driver.implicitly_wait(2)

            data_list.append({
                'Question' : question,
                'Options' : option1 + '\n' + option2 + '\n' + option3 + '\n' + option4 + '\n',
                'Answer' : answer,
                'embedding_vectors' : embedding
            })

            time.sleep(3) #혹시나 임베딩 잘못 들어가는 거 연속으로 넣기 방지

            number_of_Problems += 1

        check_test_count += 1

    # 데이터프레임 생성
    df = pd.DataFrame(data_list)

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
