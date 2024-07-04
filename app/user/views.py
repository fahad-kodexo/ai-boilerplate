import random
from passlib.context import CryptContext
from . import  schemas

from app.database.database import MongoManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users(MongoManager):
    @staticmethod
    async def get_user_by_email(email:str):
        async with Users() as db:
            user_collection = db.get_collection("users")
            return await user_collection.find_one({"email":email})
        
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def generate_reset_token() -> str:
        return str(random.randrange(100000,999999))
        
    async def create_user(user: schemas.UserCreate):
        async with Users() as db:
            hashed_password = pwd_context.hash(user.password)
            chat_collection = db.get_collection("users")
            document = {
                'email' : user.email,
                'password' : hashed_password
            }
            await chat_collection.insert_one(document) 
            return True
        
    async def verify_otp(token:str):
        async with Users() as db:
            user_collection = db.get_collection("users")
            return await user_collection.find_one({"reset_token":token})
        


    async def reset_password(token: str, new_password: str) -> bool:
        async with Users() as db:
            user_collection = db.get_collection("users")
            user = await user_collection.find_one({"reset_token":token})
            if user:
                hashed_password = pwd_context.hash(new_password)
                await user_collection.update_one({"reset_token": token}, 
                {"$set": {"reset_token": None , "password" : hashed_password}})
                return True
            return False
        

    
    async def set_reset_token(email: str):
        async with Users() as db:
            user_collection = db.get_collection("users")
            user = await Users.get_user_by_email(email)
            if user:
                token = await Users.generate_reset_token()
                await user_collection.update_one({"email": user['email']}, 
                {"$set": {"reset_token": token}})
                return token
            return None