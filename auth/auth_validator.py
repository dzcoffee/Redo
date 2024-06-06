from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from auth.jwt_utils import verify_token, refresh_token
from utils.logger import logger

class AuthValidator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthValidator, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(AuthValidator, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            new_token = refresh_token(credentials.credentials)
            if new_token:
                request.state.access_token = new_token
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = verify_token(jwtoken)
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid