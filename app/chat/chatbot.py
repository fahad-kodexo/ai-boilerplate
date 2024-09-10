import traceback
import socketio
from app.chat.schemas import Chat
from app.utils.responses import emit_response
from app.vector_db_operations.chromadb import ChromaDb
from app.vector_db_operations.openai_assistant import Assistant


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.on("user_query")
async def user_query(sid, chat: Chat):
    try:
        user_query = chat["user_query"]
        collection_name = chat["collection_name"]
        user_id = chat["user_id"]
        vector_store_client = ChromaDb(collection_name=collection_name)
        retriever = vector_store_client.get_retriever(collection_name)
        if retriever is None:
            raise Exception
        query_answer = await vector_store_client.retrieve_data_with_chat_history(
            retriever, user_query, sid, user_id
        )
        if query_answer:
            await emit_response(sio, "query_response", query_answer)
        else:
            raise Exception

    except Exception as e:
        print("Exception in user_query", e)
        await emit_response(sio, "query_response", "Something Went Wrong!")


@sio.on("user_assistant")
async def user_assistant(sid, assistant: Assistant):
    try:
        user_query = assistant["user_query"]
        thread_id = assistant["thread_id"]
        assistant_id = assistant["assistant_id"]

        await Assistant.ask_query(
            query=user_query, thread_id=thread_id, assistant_id=assistant_id, sio=sio
        )

    except Exception as e:
        print("Exception in user_assistant", traceback.print_exc())
        await emit_response(sio, "query_response", "Something Went Wrong!")
