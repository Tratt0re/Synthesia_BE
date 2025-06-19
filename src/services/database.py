# app/services/database.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from src.core.architecture import Service


class Database(Service):
    def __init__(self, mongo_url: str, db_name: str):
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None
        self._mongo_url = mongo_url
        self._db_name = db_name
        logging.info("-- MongoDB service initialized --")

    async def connect(self):
        try:
            self._client = AsyncIOMotorClient(self._mongo_url)
            self._db = self._client[self._db_name]
            logging.info("[MongoDB] Connection established.")
        except Exception as e:
            logging.error(f"[MongoDB] Connection failed: {e}")
            raise e

    async def disconnect(self):
        if self._client is not None:
            self._client.close()
            logging.info("[MongoDB] Connection closed.")

    def get_db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            raise RuntimeError("[MongoDB] Attempted to access DB before connection was established.")
        return self._db
