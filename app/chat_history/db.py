from app.database.database import MongoManager
from bson import ObjectId


class ChatHistory(MongoManager):
    async def insert_chat_history(self, user_id: str, query, assistant_message: str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")

            user_doc = {"message": query, "type": "user"}
            assistant_doc = {"message": assistant_message, "type": "assistant"}

            update_data = {
                "$push": {"chat_history": {"$each": [user_doc, assistant_doc]}}
            }
            return await user_collection.find_one_and_update(
                {"user_id": user_id}, update_data, upsert=True
            )

    async def insert_chat_user(self, email: str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            document = {"email": email, "user_id": str(ObjectId()), "chat_history": []}
            return await user_collection.insert_one(document)

    async def get_chat_history(self, user_id: str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            return await user_collection.find_one({"user_id": user_id})

    async def get_user_sessions(self, email: str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            user_ids = user_collection.find({"email": email}, {"user_id": 1, "_id": 0})

            # Iterate over the user_ids to retrieve documents
            documents = []
            async for document in user_ids:
                documents.append(document)

            return documents
