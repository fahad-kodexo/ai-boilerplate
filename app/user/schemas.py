from pydantic import BaseModel, field_validator
from fastapi import status
from fastapi.exceptions import HTTPException

class EmailValidatorModel(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, email):
        from application import ValidatorException
        if "@" not in email or "." not in email:
            raise ValidatorException(
                400,
                "Invalid Email",
                error=None
            )
        return email

class UserCreate(EmailValidatorModel):
    password: str
    first_name : str
    last_name : str

class UserLogin(EmailValidatorModel):
    password: str
    
class UserResetPassword(EmailValidatorModel):
    pass

class VerifyOTP(BaseModel):
    token: str

class UserSetNewPassword(BaseModel):
    token: str
    new_password: str
    confirm_password : str

class UserResponse(EmailValidatorModel):
    pass
