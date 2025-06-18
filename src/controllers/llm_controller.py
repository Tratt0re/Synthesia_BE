import logging
from src.services import (
    LLMService,
    TextCleanerService,
    TextExtractorService,
    JsonExtractorService,
)
from fastapi import UploadFile


class LLMController:
    def __init__(self):
        self.llm = LLMService
        self.text_extractor = TextExtractorService
        self.text_cleaner = TextCleanerService
        self.json_extractor = JsonExtractorService

    async def summarize(self, text: str, model: str, language: str = "eng") -> str:
        try:
            cleaned_text = self._clean(text)
            return await self.llm.summarize(
                text=cleaned_text,
                model=model,
                language=language,
            )
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
            raw_text = await self.text_extractor.extract_text(file)
            cleaned_text = self._clean(raw_text)

            return await self.llm.summarize(
                text=cleaned_text,
                model=model,
                language=language,
            )
        except Exception as e:
            logging.error(f"LLMController/summarize_from_file error: {e}")
            raise

    async def extract_entities(self, text: str, model: str) -> dict:
        try:
            cleaned_text = self._clean(text)
            return await self._extract_and_parse(cleaned_text, model)
        except Exception as e:
            logging.error(f"LLMController/extract_entities error: {e}")
            raise

    async def extract_entities_from_file(self, file: UploadFile, model: str) -> dict:
        try:
            raw_text = await self.text_extractor.extract_text(file)
            cleaned_text = self._clean(raw_text)
            return await self._extract_and_parse(cleaned_text, model)
        except Exception as e:
            logging.error(f"LLMController/extract_entities_from_file error: {e}")
            raise

    async def list_models(self) -> list[dict]:
        try:
            models = await self.llm.list_models()
            return [m.model_dump() for m in models]
        except Exception as e:
            logging.error(f"LLMController/list_models error: {e}")
            raise

    # ---------- PRIVATE HELPERS ----------

    def _clean(self, text: str) -> str:
        cleaned = self.text_cleaner.remove_html_tags(text)
        return self.text_cleaner.clean_text(cleaned)

    async def _extract_and_parse(self, text: str, model: str) -> dict:
        raw_output = await self.llm.extract_entities(text=text, model=model)
        parsed = self.json_extractor.extract_json(raw_output, repair=True)

        if not parsed:
            logging.warning("LLMController/_extract_and_parse: failed to parse result")
            return {"raw_response": raw_output}

        return parsed
