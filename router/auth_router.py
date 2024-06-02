from fastapi import APIRouter, Depends
from starlette import status
from utils.logger import logger
from auth import jwt_utils as JWT

router = APIRouter(
    prefix="/auth"
)
