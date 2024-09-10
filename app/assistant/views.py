from app.utils.responses import success_response, error_response, unauthorized_response
from app.vector_db_operations.openai_assistant import Assistant
from app.utils.s3_utils import S3
from fastapi import Request
from . import schemas
import os
import traceback


async def create_assistant(request: Request):
    try:
        assistant = await Assistant.create_assistant()
        if assistant is None:
            return unauthorized_response("Assistant Not Created")
        else:
            return success_response("Assistant Created", assistant)
    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))


async def create_thread(request: Request):
    try:
        thread = await Assistant.create_thread()
        if thread is None:
            return unauthorized_response("Thread Not Created")
        else:
            return success_response("Thread Created!", data=thread)

    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))


async def upload_files(request: Request, file: schemas.UploadDocument):
    try:
        local_directory_path = f"app/data/{file.user_id}/"
        os.makedirs(local_directory_path, exist_ok=True)
        local_file_path = local_directory_path + file.s3_path.split("/")[-1]
        s3_status = S3.download_file_from_s3(file.s3_path, local_file_path)
        if s3_status:
            response = await Assistant.upload_files(
                vector_store_name=file.vectorstore_name,
                file_paths=local_file_path,
                assistant_id=file.assistant_id,
            )
            if response is None:
                return unauthorized_response("File Not Uploaded on Vector Store")
            else:
                return success_response("File Uploaded Successfully")
        else:
            return unauthorized_response("File Not Uploaded on S3")

    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))
