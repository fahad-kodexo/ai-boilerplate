from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chat.chatbot import sio
import socketio

from app.cloud_functions.routes import s3_router
from app.user.routes import auth_router
from app.chat.routes import chat_router
from app.stripe_payment.routes import stripe_router
from app.assistant.routes import assistant_router
from app.chat_history.routes import chat_history_router

from app.utils.responses import success_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return success_response("Hello World!")

app.include_router(auth_router)
app.include_router(s3_router)
app.include_router(chat_router)
app.include_router(stripe_router)
app.include_router(assistant_router)
app.include_router(chat_history_router)
app.mount("/socket.io", socketio.ASGIApp(sio))
