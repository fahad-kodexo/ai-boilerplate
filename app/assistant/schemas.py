from pydantic import BaseModel

class UploadDocument(BaseModel):
    vectorstore_name : str
    user_id : str
    assistant_id : str
    s3_path :str
