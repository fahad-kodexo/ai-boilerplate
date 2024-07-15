from fastapi import APIRouter
from .views import get_chat_history,create_chat_user


chat_history_router = APIRouter(prefix="/chat_history")
chat_history_router.get("/get_chat_history")(get_chat_history)
chat_history_router.post("/create_chat_user")(create_chat_user)