from fastapi import APIRouter

from .views import (create_assistant,
                    create_thread,
                    upload_files)

assistant_router = APIRouter(prefix="/assistant")

assistant_router.post("/create_assistant")(create_assistant)
assistant_router.post("/create_thread")(create_thread)
assistant_router.post("/upload_files")(upload_files)
