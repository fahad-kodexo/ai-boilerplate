from pydantic import BaseModel

class UserChat(BaseModel):
   email : str
   