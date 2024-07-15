from app.database.database import MongoManager


class UserPayment(MongoManager):
    async def insert_user_payment(self, customer_id : str, status : str):
        async with UserPayment() as db:
            user_collection = db.get_collection("payments")
            document = {
                "customer_id" : customer_id,
                "status" : status
                }
            return await user_collection.insert_one(document)
        
    async def update_user_status(self,customer_id : str, status : str):
        async with UserPayment() as db:
            user_collection = db.get_collection("payments")
            updated_status = {
                "$set" : {
                "status": status
                }
            }
            await user_collection.find_one_and_update(
                {"customer_id": customer_id},
                updated_status
            )

            return True
            