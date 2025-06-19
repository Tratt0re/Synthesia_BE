from enum import Enum
from typing import Optional, List


class PromptTemplate(str, Enum):
    SUMMARIZE = "summarize"
    EXTRACT_ENTITIES = "extract_entities"

    def resolve(
        self,
        language: str = "eng",
        entities: Optional[List[str]] = None,
    ) -> str:
        match self:
            case PromptTemplate.SUMMARIZE:
                prompt = (
                    "Read the following text and generate a clear and concise summary that captures the most important information. "
                    "The summary should be factual, avoid repetition, and must not include any introduction, commentary, explanation, or additional notes. "
                )
                prompt += self._language_instruction(language)
                return prompt

            case PromptTemplate.EXTRACT_ENTITIES:
                if entities:
                    entity_list = ", ".join(entities)
                    prompt = (
                        f"You must extract the following entities from the provided text: {entity_list}. "
                        f"Output strictly a valid JSON object using these entities as top-level keys. "
                        f"If some of these entities are not present, include them with `null` value. "
                        f"Any additional relevant information not covered by these keys must be grouped under a separate key named `other_info`. "
                        f"Do not include any text or explanations outside of the JSON object."
                    )
                else:
                    prompt = (
                        "Extract the key entities from the following text. "
                        "Return the result strictly as a JSON object with key-value pairs. "
                        "Do not include explanations or extra text outside the JSON."
                    )
                return prompt

            case _:
                raise ValueError(f"Unsupported prompt type: {self}")

    def _language_instruction(self, language: str) -> str:
        match language.lower():
            case "ita":
                return " The output language must be Italian."
            case "eng":
                return " The output language must be English."
            case "es":
                return " The output language must be Spanish."
            case "fr":
                return " The output language must be French."
            case _:
                raise ValueError(f"Unsupported language: {language}")
