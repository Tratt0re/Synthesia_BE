from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    environment: str
    logging_format: str = "%(asctime)s %(levelname)s -> %(message)s"
    logging_level: str = "INFO"
    logging_date_format: str = "%H:%M:%S"

    upload_folder: str = "./"
    download_folder: str = "./"

    mongodb_url: str
    mongodb_db_name: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return Config()
