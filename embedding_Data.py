from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

from openai import OpenAI

import pandas as pd
import os

file_path = "./problems.csv"

model = 'text-embedding-3-small'

OPENAI_API_KEY = "sk-proj-p5uN3gZ9BbVgJGkJIE4OT3BlbkFJJ5y6pvXgzRFYYrcTopyk"
client = OpenAI(
    api_key=OPENAI_API_KEY
)

driver = webdriver.Chrome()

count = 0
while 1:

    driver.get("https://www.comcbt.com/cbt/modeselect.php?hack_number=0&h_db=iz")

    driver.implicitly_wait(2)

    cbt_page = driver.find_element(by=By.XPATH , value="/html/body/table[1]/tbody/tr[2]/td[3]/form/input[3]")

    cbt_page.click()

    driver.implicitly_wait(2)

    cbt_options1 = driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[1]/td/form/p/select")
    select1 = Select(cbt_options1)
    select1.select_by_value('기사')
    cbt_options_select1 = driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[1]/td/form/p/input[3]")
    cbt_options_select1.click()

    driver.implicitly_wait(2)
    time.sleep(3)

    cbt_options2 = driver.find_element(by=By.XPATH, value= "/html/body/table/tbody/tr/td/form/p/select")
    select2 = Select(cbt_options2)
    select2.select_by_visible_text("정보처리기사") 
    cbt_options_select2 = driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/form/p/input[3]")
    cbt_options_select2.click()

    driver.implicitly_wait(2)
    cbt_options3 = driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/form/p/select")
    select3 = Select(cbt_options3)

    options_count = len(select3.options)
    if count >= options_count: #한정된 옵션갯수까지만 수집
        break

    select3.select_by_index(count)

    cbt_options_select3 = driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/form/p/input[5]")
    cbt_options_select3.click()

    driver.implicitly_wait(2)
    
    number_of_Problems = 1

    data_list = []

    while number_of_Problems <= 100:
        question = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/table[1]/tbody/tr/td[2]").text
        option1 = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/table[2]/tbody/tr/td[2]").text
        option2 = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/table[3]/tbody/tr/td[2]").text
        option3 = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/table[4]/tbody/tr/td[2]").text
        option4 = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/table[5]/tbody/tr/td[2]").text
        answer_view = driver.find_element(by=By.XPATH, value=f"/html/body/table[{number_of_Problems}]/tbody/tr/td/input")
        answer_view.click()
        answer = driver.find_element(by=By.XPATH, value="/html/body/table[1]/tbody/tr/td/font[1]/div").text
        
        gpt_embeddings_input = question + '\n1)' + option1 + '\n2)' + option2 + '\n3)' + option3 + '\n4)' + option4

        res = client.embeddings.create(
            input = gpt_embeddings_input,
            model = 'text-embedding-3-small'
        )

        embedding = res.data[0].embedding

        print(embedding)

        driver.implicitly_wait(2)

        data_list.append({
            'Question' : question,
            'embedding_vectors' : embedding
        })

        time.sleep(1) #혹시나 임베딩 잘못 들어가는 거 연속으로 넣기 방지

        number_of_Problems += 1


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

    count += 1

