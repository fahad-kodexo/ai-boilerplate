import traceback
from functools import wraps

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.utils.email_utils import Email
from app.user.db import Users
from app.utils.jwt_utils import generate_jwt, secure
from app.utils.responses import JSONResponse, error_response, success_response

from . import schemas

templates = Jinja2Templates(directory="app/templates")

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


async def register_user(user: schemas.UserCreate, request:Request) -> JSONResponse:
    try:
        db_user = await Users.get_user_by_email(email=user.email)
        if db_user:
            return error_response("Email already registered")
        else:
            db_user = await Users.create_user(user=user)
            return success_response("User Created")
    except Exception as e:
        print("Exception in register_user",traceback.print_exc())
        return error_response(repr(e))


async def login_user(user: schemas.UserLogin) -> JSONResponse:
    try:
        db_user = await Users.get_user_by_email(email=user.email)
        if not db_user or not Users.verify_password(user.password,
                                                    db_user["password"]):
            return error_response("Incorrect email or password")

        token,expiration_time = generate_jwt()

        response = JSONResponse({"token":token}, 200)
        response.set_cookie("token",token,expires=expiration_time)

        return response
    except Exception as e:
        print("Exception in login_user",traceback.print_exc())
        return error_response(repr(e))


async def forget_password(request: Request,user: schemas.UserResetPassword,
                    ) -> JSONResponse:
    try:
        token = await Users.set_reset_token(user.email)

        if token:
            reset_link = "link"
            html_template = templates.TemplateResponse("reset_password.html",
                                                        {"request": request,
                                                        "reset_link": reset_link}).body.decode("utf-8")
            status = Email.send_email(user.email,html_template)

            if status:
                return success_response(f"Password reset email sent.")
            else:
                return error_response(f"Password reset email not send.")
        else:
            return error_response("Email Not Found")
    except Exception as e:
        print("Exception in forget_password",traceback.print_exc())
        return error_response(repr(e))


async def verify_otp(request: Request,user: schemas.VerifyOTP) -> JSONResponse:
    try:
        success = await Users.verify_otp(user.token)
        if success:
            return success_response("Valid OTP")
        else:
            return error_response("Invalid OTP")
    except Exception as e:
        print("Exception in verify_otp",traceback.print_exc())
        return error_response(repr(e))


async def reset_password(request: Request,user: schemas.UserSetNewPassword,
                   ) -> JSONResponse:
    try:
        success = await Users.reset_password(user.token, user.new_password)
        if success:
            return success_response("Password Reset Successful")
        else:
            return error_response("Invalid Reset Token")
    except Exception as e:
        print("Exception in reset_password",traceback.print_exc())
        return error_response(repr(e))
