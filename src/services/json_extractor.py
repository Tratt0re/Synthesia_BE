import json
import logging
import re
from typing import Any, Optional

from demjson3 import decode as demjson_decode
from src.core.architecture import Service


class JsonExtractor(Service):
    def __init__(self):
        logging.info("-- JsonExtractor service initialized --")

    def extract_json(
        self, raw_text: str, repair: bool = False
    ) -> Optional[dict[str, Any]]:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            pass

        # Try to extract a JSON-like object from within the string
        try:
            match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as err:
            logging.warning(f"JsonExtractor regex-based parse failed: {err}")

        # fallback on demjson3 repair json capabilities
        if repair:
            try:
                return demjson_decode(raw_text)
            except Exception as err:
                logging.warning(f"JsonExtractor repair failed: {err}")

        return None
