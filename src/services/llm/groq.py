# src/services/llm/groq_service.py

import logging
from groq import AsyncGroq
from src.services.llm.base import LLMService
from src.models.default.prompt_template import PromptTemplate
from src.models.default.llm import AvailableModel


class GroqService(LLMService):
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        logging.info("-- GroqService initialized --")

    async def summarize(self, text: str, model: str, language: str = "eng") -> str:
        prompt = self._build_prompt(
            text=text,
            prompt_template=PromptTemplate.SUMMARIZE,
            language=language,
        )

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"GroqService/summarize error: {e}")
            raise

    async def extract_entities(
        self, text: str, model: str, entities: list[str] = None
    ) -> str:
        prompt = self._build_prompt(
            text=text,
            prompt_template=PromptTemplate.EXTRACT_ENTITIES,
            entities=entities,
        )

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"GroqService/extract_entities error: {e}")
            raise

    async def list_models(self):
        raw_models = await self.client.models.list()
        return [AvailableModel(model=m.id, **m.model_dump()) for m in raw_models.data]
