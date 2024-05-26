
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.memo import memo_router
from domain.user import user_router
from domain.problem import problem_router
from domain.quiz import quiz_router
from router import auth_router
from database import Base, engine
import router.auth_router

app = FastAPI()

origins = [
    "https://redo:80", # 서버 배포 내부 도메인
    "https://port-0-redoback-1ru12mlvuze1ma.sel5.cloudtype.app", # 서버 배포 도메인
    "https://web-redo-1ru12mlvuze1ma.sel5.cloudtype.app", # 클라이언트 배포 도메인
    "http://localhost:5173" # 로컬 클라이언트 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(memo_router.router)
app.include_router(user_router.router)
app.include_router(quiz_router.router)
app.include_router(problem_router.router)
app.include_router(auth_router.router)

Base.metadata.create_all(engine)


#@app.get("/")
#def hi():
#    return {"message": "gd"}
