from abc import ABC, abstractmethod
from src.models.default.prompt_template import PromptTemplate


class LLMService(ABC):
    @abstractmethod
    async def summarize(
        self,
        text: str,
        model: str,
        language: str = "eng",
    ) -> str:
        pass

    @abstractmethod
    async def extract_entities(
        self,
        text: str,
        model: str,
        entities: list[str] = None,
    ) -> str:
        pass

    @abstractmethod
    async def list_models(self) -> list[any]:
        pass

    def _build_prompt(
        self,
        text: str,
        prompt_template: PromptTemplate = PromptTemplate.SUMMARIZE,
        language: str = "eng",
        entities: list[str] = None,
    ) -> str:
        base_instruction = prompt_template.resolve(language, entities)
        return f"{base_instruction}\n\n{text}"
