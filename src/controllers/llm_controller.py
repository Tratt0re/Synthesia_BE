import logging
from src.services import (
    LLMService,
    TextCleanerService,
    TextExtractorService,
    JsonExtractorService,
)
from fastapi import UploadFile
from typing import Optional, Union
import asyncio


class LLMController:
    def __init__(self):
        self.llm = LLMService
        self.text_extractor = TextExtractorService
        self.text_cleaner = TextCleanerService
        self.json_extractor = JsonExtractorService

    async def summarize(
        self,
        model: str,
        language: str = "eng",
        text: Optional[str] = None,
        file: Optional[UploadFile] = None,
    ) -> dict[str, str]:
        try:
            if file:
                raw_text = await self.text_extractor.extract_text(file=file)
            elif text:
                raw_text = text
            else:
                raise ValueError(
                    "Either text or file must be provided for summarization"
                )

            cleaned_text = self._clean(raw_text)
            summary = await self.llm.summarize(
                text=cleaned_text,
                model=model,
                language=language,
            )

            return {
                "summary": summary,
                "cleaned_input": cleaned_text,
            }

        except Exception as e:
            logging.error(f"LLMController/summarize error: {e}")
            raise

    async def extract_entities(
        self,
        model: str,
        text: Optional[str] = None,
        file: Optional[UploadFile] = None,
        entities: Optional[list[str]] = None,
    ) -> dict[str, Union[str, dict]]:
        try:
            if file:
                raw_text = await self.text_extractor.extract_text(file=file)
            elif text:
                raw_text = text
            else:
                raise ValueError(
                    "Either text or file must be provided for entity extraction"
                )

            cleaned_text = self._clean(raw_text)
            extracted = await self._extract_and_parse(
                text=cleaned_text,
                model=model,
                entities=entities,
            )

            return {
                "entities": extracted,
                "cleaned_input": cleaned_text,
            }

        except Exception as e:
            logging.error(f"LLMController/extract_entities error: {e}")
            raise

    async def analyze(
        self,
        model: str,
        language: str = "eng",
        text: Optional[str] = None,
        file: Optional[UploadFile] = None,
        entities: Optional[list[str]] = None,
    ) -> dict[str, Union[str, dict]]:
        """
        Run both summarization and entity extraction concurrently.
        """
        try:
            if not text and not file:
                raise ValueError("Either text or file must be provided for analysis")

            # Use the same text (extracted or passed) for both summarization and entity extraction
            if file:
                raw_text = await self.text_extractor.extract_text(file=file)
            else:
                raw_text = text

            cleaned_text = self._clean(raw_text)

            # Run both operations concurrently
            summary_result, entities_result = await asyncio.gather(
                self.llm.summarize(
                    text=cleaned_text,
                    model=model,
                    language=language,
                ),
                self._extract_and_parse(
                    text=cleaned_text,
                    model=model,
                    entities=entities,
                ),
            )

            return {
                "summary": summary_result,
                "entities": entities_result,
                "cleaned_input": cleaned_text,
            }

        except Exception as e:
            logging.error(f"LLMController/analyze error: {e}")
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

    async def _extract_and_parse(
        self,
        text: str,
        model: str,
        entities: list[str] = None,
    ) -> dict:
        raw_output = await self.llm.extract_entities(
            text=text,
            model=model,
            entities=entities,
        )
        parsed = self.json_extractor.extract_json(raw_output, repair=True)

        if not parsed:
            logging.warning("LLMController/_extract_and_parse: failed to parse result")
            return {"raw_response": raw_output}

        return parsed
