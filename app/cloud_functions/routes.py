import traceback

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi_versionizer import api_version

from app.cloud_functions.schemas import DownloadFile, UploadFile
from app.modules.s3_operations.s3_function import S3
from app.user.routes import require_token
from app.utils.responses import error_response, success_response

router = APIRouter(prefix="/file")

@router.post("/upload-file")
@api_version(1)
@require_token
def upload_file(request: Request,upload_file : UploadFile,
                      ):
    try:
        status_code = S3.generate_presigned_post(
            upload_file.file_path,
            upload_file.folder_path
        )
        if status_code == 204:
            return success_response(msg="File Uploaded")
        else:
            return error_response(msg="File Not Uploaded",status_code=400)
    except Exception as e:
        print("Exception in upload_file",traceback.print_exc())
        return error_response(msg=f"err in upload_file : {e}",status_code=400)
    

@router.post("/download-file")
@api_version(1)
@require_token
def download_file(request: Request,download_file : DownloadFile,
                        ):
    try:
        download_url = S3.generate_presigned_url(
            download_file.folder_path+"/"+download_file.file_path
            )
        return success_response(msg=download_url)
    except Exception as e:
        print("Exception in download_file",traceback.print_exc())
        return error_response(msg=f"err in download_file : {e}",status_code=400)