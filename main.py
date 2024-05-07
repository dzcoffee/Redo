
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.memo import memo_router
from domain.user import user_router
from domain.problem import problem_router
from domain.quiz import quiz_router
from database import Base, engine

app = FastAPI()

origins = [
    "http://redo:80",
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

Base.metadata.create_all(engine)


#@app.get("/")
#def hi():
#    return {"message": "gd"}
