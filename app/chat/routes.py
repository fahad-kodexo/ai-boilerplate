import traceback,os

from fastapi import Request
from fastapi.routing import APIRouter

from app.chat.schemas import AddDocument,AddText
from app.modules.s3_operations.s3_function import S3
from app.modules.vector_db_operations.chromadb import ChromaDb
from app.user.routes import require_token
from app.utils.responses import error_response, success_response

router = APIRouter(prefix="/chat")

@router.post("/add_documents")
@require_token
def add_documents(request: Request,
                  upload_data : AddDocument):
    try:
        local_directory_path = f"app/data/{upload_data.user_id}/"
        os.makedirs(local_directory_path,exist_ok=True)
        local_file_path = local_directory_path + upload_data.s3_file_path.split("/")[-1]
        s3_status = S3.download_file_from_s3(upload_data.s3_file_path,local_file_path)
        if s3_status:
            vector_client = ChromaDb(collection_name=upload_data.user_id)
            status = vector_client.add_documents(local_file_path,upload_data.user_id)
            if status:
                return success_response(msg="File Added in Db")
            else:
                return error_response(msg="File Not Added in Db",status_code=400)
        else:
            return error_response(msg="Invalid S3 Url",status_code=400)
    except Exception as e:
        print("Exception in add_documents",traceback.print_exc())
        return error_response(msg=f"err in add_documents : {e}",status_code=400)


@router.post("/add_texts")
@require_token
def add_texts(request: Request,
                upload_text : AddText):
    try:
        vector_client = ChromaDb(collection_name=upload_text.user_id)
        status = vector_client.add_texts(upload_text.text,upload_text.user_id)
        if status:
            return success_response(msg="Data Added to Db!")
        else:
            return error_response(msg="Data not Added to Db!",status_code=400)
    except Exception as e:
        print("Exception in add_texts",traceback.print_exc())
        return error_response(msg=f"err in add_texts : {e}",status_code=400)


