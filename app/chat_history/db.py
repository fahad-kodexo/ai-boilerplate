from app.database.database import MongoManager
from bson import ObjectId

class ChatHistory(MongoManager):
    async def insert_chat_history(self,user_id:str,message:str,role:str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            chat_data = await user_collection.find_one({"user_id":user_id})
            if "chat_history" not in chat_data.keys():
                chat_data = []
            else:
                chat_data = list(chat_data["chat_history"])
            chat_data.append(
                {
                    "message" : message,
                    "type" : role
                }
            )
            document = {
                "$set" : {
                "chat_history": chat_data
                }
            }
            return await user_collection.find_one_and_update({"user_id":user_id},document)
        

    async def insert_chat_user(self,email:str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            document = {
                "email" : email,
                "user_id" : str(ObjectId())
            }
            return await user_collection.insert_one(document)
        
    
    async def get_chat_history(self,user_id:str):
        async with ChatHistory() as db:
            user_collection = db.get_collection("chat_historyy")
            return await user_collection.find_one({"user_id": user_id})