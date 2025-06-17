# app/services/__init__.py

from src.core.config import get_config
from src.services.database import Database
from src.services.text_cleaner import TextCleaner
from src.services.llm.ollama import LocalOllamaService
from src.services.llm.base import LLMService as LLMServiceBase
from src.services.text_extractor import TextExtractor


def init_database() -> Database:
    config = get_config()
    return Database(mongo_url=config.mongodb_url, db_name=config.mongodb_db_name)


def init_text_cleaner() -> TextCleaner:
    return TextCleaner()


def init_text_extractor() -> TextExtractor:
    return TextExtractor()


def init_llm_service() -> LLMServiceBase:
    return LocalOllamaService(host="http://localhost:11434")


LLMService: LLMServiceBase = init_llm_service()
DatabaseService: Database = init_database()
TextCleanerService: TextCleaner = init_text_cleaner()
TextExtractorService: TextExtractor = init_text_extractor()
