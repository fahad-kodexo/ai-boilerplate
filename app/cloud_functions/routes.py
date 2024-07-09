from fastapi import APIRouter

from .views import (download_file,
                    upload_file
                    )

s3_router = APIRouter()
s3_router.prefix("/file")

s3_router.post("/upload_file")(upload_file)
s3_router.post("/download_file")(download_file)
