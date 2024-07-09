import datetime

import jwt

from app.utils.constants import JWT_ALGORITHM, SECRET_KEY


def secure(token:str) -> bool:
    try:
        _ = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        return True
    except Exception:
        return False


def generate_jwt(expiration_minutes=30) -> tuple[str,datetime.datetime]:
    date_format = "%Y-%m-%d %H:%M:%S"
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    payload = {
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    expiration_time = expiration_time.strftime(date_format)
    return token,expiration_time
