from abc import ABC, abstractmethod

class LLMService(ABC):
    @abstractmethod
    async def summarize(self, text: str, model: str, language: str = "eng") -> str:
        pass

    @abstractmethod
    async def extract_entities(self, text: str, model: str) -> str:
        pass

    @abstractmethod
    async def list_models(self) -> list[any]:
        pass
