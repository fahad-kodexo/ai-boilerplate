
import socketio
from app.chat.schemas import Chat
from app.modules.vector_db_operations.chromadb import ChromaDb


sio = socketio.AsyncServer(async_mode="asgi",cors_allowed_origins="*")

@sio.event
async def user_query(sid, chat:Chat):
    user_query = chat.user_query
    collection_name = chat.collection_name
    vector_store_client = ChromaDb(collection_name=collection_name)
    retriever = vector_store_client.get_retriever(collection_name)
    query_answer = vector_store_client.retrieve_data_with_chat_history(retriever,user_query,sid)
    if query_answer:
        response = {
            "status": "success",
            "message": f"Answer: {query_answer}"
        }
    else:
        response = {
            "status" : "fail",
            "message" : "Something Went Wrong"
        }
    return response




