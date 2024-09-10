import datetime
from functools import wraps
from fastapi import Request
from app.utils.responses import error_response

import jwt, re

from app.utils.constants import JWT_ALGORITHM, SECRET_KEY


def secure(token: str) -> bool:
    try:
        _ = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        return True
    except Exception:
        return False


def generate_jwt(user_id: str, expiration_minutes=30) -> tuple[str, datetime.datetime]:
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=expiration_minutes
        )
        payload = {"exp": expiration_time, "user_id": user_id}
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        expiration_time = expiration_time.strftime(date_format)
        return token, expiration_time
    except Exception as e:
        print("Error in generate_jwt", e)
        return None


async def jwt_cookie_token(request: Request):
    from application import TokenException

    token = request.headers.get("authorization").split(" ")[1]
    if not token:
        raise TokenException(status_code=401, detail="Token is missing", error=None)

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise TokenException(
            status_code=401, detail="The token has expired.", error=None
        )
    except jwt.InvalidTokenError:
        raise TokenException(
            status_code=401, detail="The token is invalid.", error=None
        )


async def validate_password(password):
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    return True, password
