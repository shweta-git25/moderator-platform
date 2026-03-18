import jwt
import os
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str):

    try:
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload_data

    except ExpiredSignatureError:
        raise Exception("Token expired")

    except InvalidTokenError:
        raise Exception("Invalid token")