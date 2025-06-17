import logging
from src.services import LLMService, TextCleanerService, TextExtractorService
from typing import List, Dict, Any
from fastapi import UploadFile


class LLMController:
    def __init__(self):
        self.llm = LLMService
        self.extractor = TextExtractorService
        self.cleaner = TextCleanerService

    async def summarize(self, text: str, model: str, language: str = "eng") -> str:
        try:
            return await self.llm.summarize(text=text, model=model, language=language)
        except Exception as e:
            logging.error(f"LLMController/summarize error: {e}")
            raise

    async def summarize_from_file(
        self,
        file: UploadFile,
        model: str,
        language: str,
    ) -> str:
        try:
            # Extract raw text from file
            raw_text = await self.extractor.extract_text(file)

            # Clean and sanitize text
            cleaned_text = self.cleaner.remove_html_tags(raw_text)
            cleaned_text = self.cleaner.clean_text(cleaned_text)

            # Summarize
            return await self.llm.summarize(
                text=cleaned_text,
                model=model,
                language=language,
            )

        except Exception as e:
            logging.error(f"LLMController/summarize_from_file error: {e}")
            raise

    async def list_models(self) -> list[dict]:
        try:
            models = await self.llm.list_models()

            # Convert AvailableModel → dict
            return [m.model_dump() for m in models]
        except Exception as e:
            logging.error(f"LLMController/list_models error: {e}")
            raise
