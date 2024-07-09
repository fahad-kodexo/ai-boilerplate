
from fastapi.responses import JSONResponse


def success_response(msg:str) -> JSONResponse:
    return JSONResponse(content=msg,status_code=200)


def error_response(msg:str) -> JSONResponse:
    return JSONResponse(content=msg,status_code=401)
