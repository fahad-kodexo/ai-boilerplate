from fastapi import APIRouter

from .views import add_documents, add_texts

chat_router = APIRouter(prefix="/chat")
chat_router.post("/add_documents")(add_documents)
chat_router.post("/add_texts")(add_texts)
