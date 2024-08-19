import traceback,os

from fastapi import Request

from app.chat.schemas import AddDocument,AddText
from app.utils.s3_utils import S3
from app.vector_db_operations.chromadb import ChromaDb
from app.utils.responses import error_response, success_response, unauthorized_response


def add_documents(request: Request,
                  upload_data : AddDocument):
    try:
        local_directory_path = f"app/data/{upload_data.user_id}/"
        os.makedirs(local_directory_path,exist_ok=True)
        local_file_path = local_directory_path + upload_data.s3_file_path.split("/")[-1]
        s3_status = S3.download_file_from_s3(upload_data.s3_file_path,
                                             local_file_path)
        if s3_status:
            vector_client = ChromaDb(collection_name=upload_data.user_id)
            status = vector_client.add_documents(local_file_path,
                                                 upload_data.user_id)
            if status:
                return success_response(msg="File Added in Db")
            else:
                return unauthorized_response("Document Not Added in the Vector Database")
        else:
            return unauthorized_response("File Not Uploaded on S3")
    except Exception as e:
        print("Exception in add_documents",traceback.print_exc())
        return error_response(repr(e))



def add_texts(request: Request,
              upload_text : AddText):
    try:
        vector_client = ChromaDb(collection_name=upload_text.user_id)
        status = vector_client.add_texts(upload_text.text,
                                         upload_text.user_id)
        if status:
            return success_response(msg="Data Added to Db")
        else:
            return unauthorized_response("Data Not Added in Vector Store")
    except Exception as e:
        print("Exception in add_texts",traceback.print_exc())
        return error_response(repr(e))
