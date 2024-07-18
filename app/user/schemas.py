from pydantic import BaseModel, field_validator
from fastapi import status
from fastapi.exceptions import HTTPException

class EmailValidatorModel(BaseModel):
    email: str
    
    @field_validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            raise HTTPException(detail="Invalid Email Address",
                                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return email

class UserCreate(EmailValidatorModel):
    password: str

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
