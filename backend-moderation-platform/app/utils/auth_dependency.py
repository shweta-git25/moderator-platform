from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_handler import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = verify_token(token)
        return payload

    except Exception as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )