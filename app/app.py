from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chat.socket import sio
import socketio

# Import routes
from app.cloud_functions.routes import router as s3_router
from app.user.routes import router as user_router
from app.chat.routes import router as chat_router

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

# Include route in your app
app.include_router(user_router)
app.include_router(s3_router)
app.include_router(chat_router)
app.mount("/socket.io", socketio.ASGIApp(sio))
