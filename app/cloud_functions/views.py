import traceback

from fastapi import Request

from app.cloud_functions.schemas import DownloadFile, UploadFile
from app.utils.s3_utils import S3
from app.user.views import require_token
from app.utils.responses import error_response, success_response

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
            raise Exception
    except Exception as e:
        print("Exception in upload_file",traceback.print_exc())
        return error_response(repr(e))


@require_token
def download_file(request: Request,
                  download_file : DownloadFile):
    try:
        download_url = S3.generate_presigned_url(
            download_file.folder_path+"/"+download_file.file_path
            )
        if download_url is None:
            raise Exception
        return success_response(msg=download_url)
    except Exception as e:
        print("Exception in download_file",traceback.print_exc())
        return error_response(repr(e))
