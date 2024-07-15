from pydantic import BaseModel

class Customer(BaseModel):
    name : str
    email: str

class CheckoutSession(BaseModel):
    customer_id : str
    price_id : str

class PortalSession(BaseModel):
    session_id : str