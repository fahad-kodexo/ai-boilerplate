# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from app.utils.constants import SQLALCHEMY_DATABASE_URL

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

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