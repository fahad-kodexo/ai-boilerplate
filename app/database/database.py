from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.constants import DB_NAME, MONGO_URI


class MongoManager:
    def __init__(self):
        self.client = None
        self.db = None
    async def __aenter__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        return self.db
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
