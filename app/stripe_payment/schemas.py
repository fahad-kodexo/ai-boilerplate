from pydantic import BaseModel,field_validator
from fastapi import status
from fastapi.exceptions import HTTPException

class Customer(BaseModel):
    name : str
    email: str
    @field_validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            print("Invalid Email")
            raise HTTPException(detail="Invalid Email Address",
                                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return email

class CheckoutSession(BaseModel):
    customer_id : str
    price_id : str

class PortalSession(BaseModel):
    session_id : str
