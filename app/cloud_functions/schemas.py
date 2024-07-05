from pydantic import BaseModel


class DownloadFile(BaseModel):
    folder_path: str
    file_path: str

class UploadFile(BaseModel):
    folder_path: str
    file_path: str
