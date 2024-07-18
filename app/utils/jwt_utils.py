import datetime
from functools import wraps
from fastapi import Request
from app.utils.responses import error_response

import jwt

from app.utils.constants import JWT_ALGORITHM, SECRET_KEY


def secure(token:str) -> bool:
    try:
        _ = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        return True
    except Exception:
        return False


def generate_jwt(expiration_minutes=30) -> tuple[str,datetime.datetime]:
    try:
        date_format = "%Y-%m-%d %H:%M:%S"
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
        payload = {
            "exp": expiration_time
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        expiration_time = expiration_time.strftime(date_format)
        return token,expiration_time
    except Exception as e:
        print("Error in generate_jwt",e)
        return None

def require_token(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        request: Request = kwargs["request"]
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None or not authorization_header.startswith("Bearer "):
            return error_response("Authorization header missing or invalid")

        token = authorization_header.split(" ")[1]
        jwt_status = secure(token)

        if jwt_status is False:
            return error_response("Unauthorized Access")
        request.state.user = jwt_status

        return f(*args, **kwargs)

    return check_token