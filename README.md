# Redo

본 프로젝트는 **GPT에게 기록한 메모를 복습하고 정리할 수 있는 서비스**입니다.
오랫동안 기록해 메모가 쌓이면 특정 개념을 어디에 기록했는지 찾기 어려워집니다.

**‘Redo’가 제공하는 퀴즈**와 함께하면 문제없이 모든 기록을 복습 받을 수 있습니다.
이 ‘Redo’ 서비스는 **Computer Science에 특화**되어 있으며 관련 학문을 학습하는 이들에게 큰 도움이 될 것입니다.


# 주요 특징:
## 전반적인 시스템 Diagram
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/a7a37d5f-d102-4bd5-a937-c0689f87fb62)


- 크게 **메모/퀴즈생성/ 퀴즈 정답 검증**  3단계로 구분됩니다.
- 각각의 세부적인 Logic에 대한 설명은 **최종발표 자료 영상 6:35 구간**부터 설명되어 있습니다.
   

## 1) 메모 카테고리 추천 기능
<details>
<summary> 메모 카테고리 추천 기능 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/fa0a9caf-3684-4083-8111-e757820e3404)
</details>

- 사용자가 작성한 내용을 바탕으로 카테고리를 추천 받을 수 있습니다.
- GPT Embedding API를 이용한  카테고리 추천 Model로 사용자에게 메모 내용과 **가장 유사한 3가지 카테고리**를 추천해줍니다.
- 여기서 정해진 카테고리는 **퀴즈생성 기능**에서 중요한 역할을 합니다.

## 2) 퀴즈 생성 기능
<details>
<summary> 퀴즈 생성 기능 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/68a1e650-cecb-4420-abd3-32ef4373f0b2)
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/b6fadeea-92e2-4798-9ab3-0da8956b7906)
</details>

- GPT ChatCompletion api를 이용한 퀴즈 생성 기능입니다.
- **프롬프트 엔지니어링**을 통해 UI에서 선택한 옵션들을 적용시켜 문제를 생성해줍니다.
- 문제 난이도는 **'입문자/전공 대학생/취업준비생'** 이라는 페르소나로 나누어 구분된 문제의 난이도를 제공합니다.
- 어려움 난이도 같은 경우에는 Markdown으로 작성된 **Table이나 Code Sample**이 문제에 포함될 수 있습니다.
- 메모 등록 시, 이미 Moderation으로 검증된 메모만 퀴즈 생성에 사용할 수 있습니다.
- 문제 개수 옵션에 따라 **Embedding 문제 모델에 저장된 문제**도 GPT가 생성한 문제와 같이 풀 수 있습니다.
- 문제 생성 시 GPT 생성 문제는 질문 아래의 **유사도**를 기반이 된 **메모 내용과 메모 카테고리 Label에 해당하는 Embedding 문제 모델과의 Cosine 유사도**를 측정해 문제에 대한 검증 지표로 이용할 수 있습니다.
- 여기서 새롭게 GPT가 생성해준 문제는 사용자의 판단에 따라 재사용될 수도 있습니다.

## 3) 퀴즈 문제 풀이 및 Feedback 기능
<details>
<summary> 퀴즈 문제 풀이 및 Feedback 기능 </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/7905bcf8-5d29-482b-9604-2e694df7b65b)
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/d5f25ba2-2106-41a6-b35f-779bb5b386c7)
</details>


- 문제에 대한 답을 작성하고 정답보기 버튼을 클릭하시면 내부 로직에 따라 **객관식은 자체적으로 정답 검증 후 풀이를 제공하고 단답식/주관식은 질문과 유저의 답변을 ChatCompletion api에 넣어 답변 검증과 풀이 생성**해 제공합니다.
- 사용자가 풀이를 보고 문제에 대한 피드백을 점수로 남기면 이 점수에 따라서 GPT가 생성해준 문제를 재사용 여부를 결정하게 됩니다.
- 단답식/주관식 유저 답변에도 Moderation이 적용되어 있습니다.


# 사용설명 :
## 주의사항

- 배포 과정에서 다소 delay가 있을 수 있습니다. 만약 사용하기 너무 힘들 정도로 delay가 있을 경우 답변 남겨주세요.
- 메모 내용은 **3000자** 까지로 제한하는 것을 권장 드립니다. (그 이상도 가능은 하나 사용성이 떨어질 수 있습니다.)
- 퀴즈 생성 후에는 피드백을 제출하는 것을 권장 드립니다.
- 권장 드리는 카테고리는 **운영체제, 설계패턴, 데이터베이스, 네트워크** 순입니다.
- 퀴즈 생성하시기 전에 옵션 한 번씩 꼭 확인해주시길 바랍니다!

## 로그인/회원가입
<details>
<summary> 로그인/회원가입 Image </summary>

### 로그인
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/c2711e1a-5b47-4a02-8c17-0058e9f5807c)
### 회원가입
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/e82dba92-4f54-4565-b0d7-5818dac6c8f5)
</details>

- 회원가입 및 로그인을 통해 서비스를 이용하실 수 있습니다.
- 모든 로그인 과정은 JWT 발급 방식으로 처리되어 안전하게 이용하실 수 있습니다.
- 로그인 후 각 User마다 구분된 서비스를 이용하실 수 있습니다.

### 메모 등록/수정/삭제
<details>
<summary> 메모 등록/수정/삭제 Image </summary>

### 메모 등록
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/90e8c628-61f8-4358-bf7e-c2e00a26a4ba)
### 메모 수정/삭제
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/9f304655-9c8e-4d92-a350-0c9e49e8dddc)
</details>

- 메모를 등록하고 수정하고 삭제하실 수 있습니다.
- 메모를 등록하고 수정할 때(즉, 서버에 저장될 때)는 **Moderation 검증 과정**을 거쳐 안전한 정보만으로 서비스를 이용하실 수 있습니다.
-  Moderation 검증에 번역하는 과정이 있기 때문에 **메모 내용 길이에 따라 시간이 걸릴 수 있습니다.**
- Moderation은 메모 등록, 수정 기능 모두 적용되어 있습니다.

### 메모 카테고리 선택
<details>
<summary> 메모 카테고리 선택 Image </summary>

### 메모 카테고리 추천
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/fa0a9caf-3684-4083-8111-e757820e3404)
### 메모 직접 선택
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/42c90b32-e40b-4ea1-89ab-b82d154d43bf)
</details>

- 메모 내용과 관련 있는 카테고리를 선택해주시길 바랍니다. (퀴즈 생성에 영향을 줄 수 있습니다.)
- 카테고리는 **메모 당 하나**만 고를 수 있습니다.

### 퀴즈 생성
<details>
<summary>퀴즈 생성 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/f667fcca-101a-4fbf-86ba-7f39b0a172d5)
</details>

- 작성하신 메모를 선택해서 해당 메모 내용 기반으로 문제를 생성할 수 있습니다.
- 문제 갯수는 1~5개로 선택가능하며, **2개 이상이면 Embedding Model의 문제** 또한 이용하실 수 있습니다. (메모 내용에 따라 유사한 문제가 없을 시 오로지 GPT문제로만 생성될 수 있음)
- 문제 형식에는 객관식/단답식/주관식이 있습니다.
- 문제 난이도는 쉬움/중간/어려움으로 **어려움을 선택할 시 Code Sample이나 Table이 포함된 문제**를 푸실 수도 있습니다. (내용에 따라 포함되지 않을 수도 있음)

### 퀴즈 풀기
<details>
<summary>퀴즈 풀기 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/d6efde77-8110-47ce-8ca3-c664e4aa558a)
![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/a749b677-1d56-4555-a3db-ef8f9888a2df)
</details>

- 퀴즈가 생성되었다면 이제 퀴즈를 푸시면 됩니다!
- 퀴즈를 다 푸셨다면 정답보기 버튼을 눌러주세요

### 퀴즈 풀이
<details>
<summary>퀴즈 풀이 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/0187f864-8ec1-4b37-a298-aac2f1df6128)
</details>

- 객관식의 경우 서버의 처리만 끝나면 바로 해설을 보실 수 있습니다.
- 단답식/ 주관식의 경우 GPT API의 요청에 응답하면 해설을 보실 수 있습니다.

### 피드백
<details>
<summary>피드백 Image </summary>

![image](https://github.com/PiLab-CAU/OpenSourceProject-2401/assets/115972127/93934e3d-b58f-41af-9453-6a3747d84fe5)
</details>

- 문제를 풀고 피드백 점수를 매겨주세요!
- 피드백 점수가 높으면 다른 사람들과 함께 해당 문제를 재활용할 수 있도록 설계되어 있습니다!

## Contributor
윤도경 (@dzcoffee)
한신(@Urchinode)
박민영(@meanyong)
이혜희(@Hyehee-Lee)

---

## 커밋 규칙

| 커밋 주제    | 내용                                                       |
| ------------ | ---------------------------------------------------------- |
| **feat**     | **새로운 기능 구현 EX: 로그인 페이지, CRUD 기능**          |
| **update**   | **기존 기능 업데이트 EX: UI 변경, gpt 프롬프트 수정**      |
| **fix**      | **버그 수정**                                              |
| **refactor** | **프로젝트 폴더 구조 정리 및 코드 개선(가독성, 유지보수)** |
| **chore**    | **불필요한 파일 삭제, 폴더 구조 재배치, 임시 기능 구현**   |
| **docs**     | **문서화**                                                 |
| **config**   | **패키지 관리, 설정 파일, 기술 연동(DB 등)**               |

다음 형식의 커밋 메시지를 권장드립니다.

> [분야] 커밋 주제: 내용

```

EX)
[client] feat: 로그인 페이지 UI
[client] fix: 로그아웃 시 토큰 초기화
[server] feat: 메모 CRUD
[server] config: DB 관련 패키지 추가
[project] docs: README 수정
```

`분야`는 간단하게 프론트(`client`), 서버(`server`), 프로젝트 전체(**`project`**)로 구분하고자 합니다.

## 브랜치 규칙

| 종류                  | 용도                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **main**              | **배포용 - 배포 툴이 이 브랜치의 커밋 변경 상태를 감지해 자동 배포할 수 있게합니다.**                              |
| **dev**               | **코드 통합 - 프론트와 서버 기능을 취합할 브랜치입니다.**                                                          |
| **feature/기능 이름** | **기능 개발 - 각자가 맡은 기능을 개발할 브랜치입니다. 추후, dev에 merge하고 삭제하는 방식으로 사용하고자 합니다.** |

### 개발 과정

![개발 사이클](./docs/development-cycle.png)

#### 1. feature 브랜치 생성

```bash
git checkout -b feature/[기능 이름]

EX:
git checkout -b feature/login-ui
git checkout -b feature/memo-crud
```

**`git checkout -b`** 로 원하는 이름의 브랜치를 만든 후 이동합니다.

#### 2. 개발

로컬에서 기능을 구현합니다.

❗위의 커밋 규칙에 맞는 커밋 메시지를 따라주시면 감사하겠습니다.

❗**하나의 커밋에 너무 많은 기능이 구성되지 않도록** 적절히 나누어 커밋하는 것을 권장합니다.

#### 3. Pull Request 생성

Github 페이지에 들어와 `Pull Request`를 생성합니다.

만약, *브랜치 충돌이 발생한다면 해결*한 후 커밋합니다.

❗현재 작업하는 브랜치의 **커밋이 최신이 되도록 Pull, Push를 잊지 말아주세요!**

#### 4. Merge 진행(dev, main)

`feature` 브랜치는 `dev`에 merge합니다.

`dev` 브랜치에서 기능 상 문제가 없다면 `main`에 merge합니다.

#### 5. Pull 진행

로컬에서도 merge된 결과를 Pull해줍니다.

```bash
git pull origin main
```

#### 1 ~ 5 반복하며 진행
