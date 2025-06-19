from typing import List
from src.services.llm.base import LLMService
from src.models.default.llm import AvailableModel
from src.models.default.prompt_template import PromptTemplate
from ollama import AsyncClient
import logging


class LocalOllamaService(LLMService):
    def __init__(self, host: str = "http://localhost:11434"):
        self.client = AsyncClient(host=host)
        logging.info("-- LocalOllamaService service initialized --")

    async def summarize(self, text: str, model: str, language: str = "eng") -> str:
        prompt = self._build_prompt(
            text=text,
            prompt_template=PromptTemplate.SUMMARIZE,
            language=language,
        )

        try:
            response = await self.client.generate(
                model=model,
                prompt=prompt,
                stream=False,
            )
            return response.get("response", "").strip()
        except Exception as e:
            logging.error(f"[LocalOllamaService] summarize() failed: {e}")
            raise

    async def extract_entities(self, text: str, model: str, entities: list[str]) -> str:
        prompt = self._build_prompt(
            text=text,
            prompt_template=PromptTemplate.EXTRACT_ENTITIES,
            entities=entities,
        )

        try:
            response = await self.client.generate(
                model=model,
                prompt=prompt,
                stream=False,
            )
            return response.get("response", "").strip()
        except Exception as e:
            logging.error(f"[LocalOllamaService] summarize() failed: {e}")
            raise

    async def list_models(self) -> List[AvailableModel]:
        try:
            result = await self.client.list()
            models_raw = result.model_dump().get("models", [])

            return [
                AvailableModel(
                    model=m.get("model"),
                    parameter_size=m.get("details", {}).get(
                        "parameter_size", "unknown"
                    ),
                )
                for m in models_raw
            ]

        except Exception as e:
            logging.error(f"[LocalOllamaService] list_models() failed: {e}")
            raise
