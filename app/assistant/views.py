from app.utils.responses import success_response,error_response
from app.vector_db_operations.openai_assistant import Assistant
from app.utils.jwt_utils import require_token
from app.utils.s3_utils import S3
from fastapi import Request
from . import schemas
import os
import traceback

@require_token
async def create_assistant(request: Request):
    try:
        assistant = await Assistant.create_assistant()
        if assistant is None:
            raise Exception
        else:
            response = {
                "assistant": assistant
                }
        return success_response(response)
    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))

@require_token
async def create_thread(request: Request):
    try:
        thread = await Assistant.create_thread()
        if thread is None:
            raise Exception
        else:
            response = {
                "thread": thread
                }

        return success_response(response)
    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))

@require_token
async def upload_files(request: Request,file : schemas.UploadDocument):
    try:
        local_directory_path = f"app/data/{file.user_id}/"
        os.makedirs(local_directory_path,exist_ok=True)
        local_file_path = local_directory_path + file.s3_path.split("/")[-1]
        s3_status = S3.download_file_from_s3(file.s3_path,
                                             local_file_path)
        if s3_status:
            response = await Assistant.upload_files(
                vector_store_name = file.vectorstore_name,
                file_paths = local_file_path,
                assistant_id = file.assistant_id
            )
            if response is None:
                raise Exception
        else:
            raise Exception
        return success_response(response)
    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))

