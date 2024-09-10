from pydantic import BaseModel, field_validator
from fastapi import status
from fastapi.exceptions import HTTPException


class UserChat(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            raise HTTPException(
                detail="Invalid Email Address",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return email
