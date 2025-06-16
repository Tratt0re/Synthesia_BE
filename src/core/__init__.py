import logging
from fastapi import Depends
from typing_extensions import Annotated
from src.core.config import get_config, Config as ConfigCls


def init_logger() -> None:
    config = get_config()
    FORMAT = config.logging_format
    LEVEL = config.logging_level
    DATE_FORAT = config.logging_date_format
    logging.basicConfig(format=FORMAT, level=LEVEL, datefmt=DATE_FORAT)


init_logger()
Config = Annotated[ConfigCls, Depends(get_config)]
