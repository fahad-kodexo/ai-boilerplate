import traceback

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.utils.email_utils import Email
from app.user.db import Users

from app.utils.responses import (
    JSONResponse,
    error_response,
    success_response,
    unauthorized_response,
    not_found_response,
    bad_request_response,
    validator_response,
)
from app.utils.jwt_utils import generate_jwt, jwt_cookie_token, validate_password

from . import schemas

templates = Jinja2Templates(directory="app/templates")


async def register_user(user: schemas.UserCreate, request: Request) -> JSONResponse:
    try:
        status, password_message = await validate_password(user.password)
        if status:
            db_user = await Users.get_user_by_email(email=user.email)
            if db_user:
                return unauthorized_response("Email already registered")
            else:
                db_user = await Users.create_user(user=user)
                token, expiration_time = generate_jwt(str(db_user.inserted_id))
                json_response = {
                    "token": token,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                response = success_response(
                    msg="User Logged In Successfully!", data=json_response
                )
                response.set_cookie(
                    "token",
                    token,
                    expires=expiration_time,
                    httponly=True,
                    secure=True,
                    samesite="none",
                )

                return response
        else:
            return validator_response(password_message)

    except Exception as e:
        print("Exception in register_user", traceback.print_exc())
        return error_response(repr(e))


async def login_user(user: schemas.UserLogin) -> JSONResponse:
    try:
        db_user = await Users.get_user_by_email(email=user.email)
        if not db_user or not Users.verify_password(user.password, db_user["password"]):
            return not_found_response("Incorrect email or password")

        token, expiration_time = generate_jwt(str(db_user["_id"]))

        json_response = {
            "token": token,
            "email": user.email,
            "first_name": db_user.get("first_name"),
            "last_name": db_user.get("last_name"),
        }
        response = success_response(
            msg="User Logged In Successfully!", data=json_response
        )
        response.set_cookie(
            "token",
            token,
            expires=expiration_time,
            httponly=True,
            secure=True,
            samesite="none",
        )

        return response
    except Exception as e:
        print("Exception in login_user", traceback.print_exc())
        return error_response(repr(e))


async def forget_password(
    request: Request,
    user: schemas.UserResetPassword,
) -> JSONResponse:
    try:
        token = await Users.set_reset_token(user.email)

        if token:
            reset_link = "link"
            html_template = templates.TemplateResponse(
                "reset_password.html", {"request": request, "reset_link": reset_link}
            ).body.decode("utf-8")
            status = Email.send_email(user.email, html_template)

            if status:
                return success_response(f"Password reset email sent.")
            else:
                return unauthorized_response(f"Password reset email not send.")
        else:
            return not_found_response("Email Not Found")
    except Exception as e:
        print("Exception in forget_password", traceback.print_exc())
        return error_response(repr(e))


async def verify_otp(request: Request, user: schemas.VerifyOTP) -> JSONResponse:
    try:
        success = await Users.verify_otp(user.token)
        if success:
            return success_response("Valid OTP")
        else:
            return unauthorized_response("Invalid OTP")
    except Exception as e:
        print("Exception in verify_otp", traceback.print_exc())
        return error_response(repr(e))


async def reset_password(
    request: Request,
    user: schemas.UserSetNewPassword,
) -> JSONResponse:
    try:
        if user.new_password == user.confirm_password:
            success = await Users.reset_password(user.token, user.new_password)
            if success:
                return success_response("Password Reset Successful")
            else:
                return not_found_response("User Not Found")
        else:
            return unauthorized_response("Invalid New and Confirm Password")
    except Exception as e:
        print("Exception in reset_password", traceback.print_exc())
        return error_response(repr(e))
