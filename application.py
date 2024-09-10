from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
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


class TokenException(HTTPException):
    def __init__(self, status_code: int, detail: str, error: str = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.error = error

    def to_dict(self):
        return {
            "error": self.error,
            "message": self.detail,
            "status_code": self.status_code,
        }


class ValidatorException(HTTPException):
    def __init__(self, status_code: int, detail: str, error: str = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.error = error

    def to_dict(self):
        return {
            "error": self.error,
            "message": self.detail,
            "status_code": self.status_code,
        }


@app.exception_handler(TokenException)
async def custom_http_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(ValidatorException)
async def custom_http_exception_handler(request: Request, exc: ValidatorException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
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
