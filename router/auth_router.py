from fastapi import APIRouter, Depends
from starlette import status
from utils.logger import logger
from auth import jwt_utils as JWT

router = APIRouter(
    prefix="/auth"
)

@router.post("", status_code=status.HTTP_200_OK)
async def get_token(string: str):
    return JWT.create_token(string)