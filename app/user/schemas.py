from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResetPassword(BaseModel):
    email: str

class VerifyOTP(BaseModel):
    token : str

class UserSetNewPassword(BaseModel):
    token: str
    new_password: str

class UserResponse(BaseModel):
    email: str
