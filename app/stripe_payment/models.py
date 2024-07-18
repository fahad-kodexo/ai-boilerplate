from pydantic import BaseModel

class PaymentHistory(BaseModel):
    customer_id : str
    status : str
