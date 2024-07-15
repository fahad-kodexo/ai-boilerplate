from pydantic import BaseModel
from typing import List,Dict

class ChatHistoryModel(BaseModel):
    _id : str
    user_id : str
    chat_history : List[Dict[str, str]]