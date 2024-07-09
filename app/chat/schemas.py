from pydantic import BaseModel

class AddDocument(BaseModel):
    user_id : str
    s3_file_path: str

class AddText(BaseModel):
    text : str
    user_id : str

class Chat(BaseModel):
    user_query : str
    collection_name : str
