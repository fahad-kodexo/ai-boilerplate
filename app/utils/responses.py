
from fastapi.responses import JSONResponse

def success_response(msg, data=None):
    response_content = {"message": msg, "data": data, "status_code": 200}
    return JSONResponse(content=response_content, status_code=200)


def not_found_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 404}
    return JSONResponse(content=response_content, status_code=404)


def bad_request_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 400}
    return JSONResponse(content=response_content, status_code=400)


def unauthorized_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 401}
    return JSONResponse(content=response_content, status_code=401)


def validator_response(msg):
    response_content = {
        "error" : None,
        "message" : msg,
        "status_code" : 400
    }
    return JSONResponse(content=response_content,status_code=400)


def error_response(exception=None):
    response_content = {
        "error": repr(exception) if exception else "",
        "message": "",
        "status_code": 500,
    }
    return JSONResponse(content=response_content, status_code=500)



async def emit_response(sio,event_name:str,message:str):
    await sio.emit(
        event_name,
        {"message" : message
         }
    )
