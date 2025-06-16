# app/services/__init__.py

from src.core.config import get_config
from src.services.database import Database
from src.services.text_cleaner import TextCleaner

def init_database() -> Database:
    config = get_config()
    return Database(mongo_url=config.mongodb_url, db_name=config.mongodb_db_name)

def init_text_cleaner() -> TextCleaner:
    return TextCleaner()

DatabaseService: Database = init_database()
TextCleanerService: TextCleaner = init_text_cleaner()
