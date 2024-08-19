from bson import json_util
import traceback,json

from fastapi import Request
from app.chat_history.schemas import UserChat
from app.chat_history.db import ChatHistory
from app.utils.responses import error_response, success_response,unauthorized_response,not_found_response


async def get_chat_history(request: Request):
    try:
        user_id = str(request.query_params.get("user_id"))

        user_chat_history = await ChatHistory().get_chat_history(
                user_id
        )
        if not user_chat_history:
            return not_found_response(msg = "User History Not Found")
        
        response = {"chat_history" : user_chat_history}
        return success_response("Chat History Found",json.loads(json_util.dumps(response)))

    except Exception as e:
        print("Exception in get_chat_history",traceback.print_exc())
        return error_response(repr(e))


async def create_chat_user(request: Request,
              user_chat : UserChat):
    try:
        user =  await ChatHistory().insert_chat_user(
            user_chat.email
        )
        response = {"user_id" : user.inserted_id}

        return success_response(json.loads(json_util.dumps(response)))
    except Exception as e:
        print("Exception in create_chat_user",traceback.print_exc())
        return error_response(repr(e))


async def get_sessions_by_email(request: Request):
    try:
        email = str(request.query_params.get("email"))

        user_session = await ChatHistory().get_user_sessions(
                email
        )

        response = {"user_session_ids" : user_session}

        return success_response("Sessions Found",json.loads(json_util.dumps(response)))

    except Exception as e:
        print("Exception in get_sesssions_by_email",e)
        return error_response(repr(e))
