from enum import Enum


class PromptTemplate(str, Enum):
    SUMMARIZE = "summarize"
    EXTRACT_ENTITIES = "extract_entities"

    def resolve(self, language: str = "eng") -> str:
        match self:
            case PromptTemplate.SUMMARIZE:
                prompt = "Summarize the following text in a clear and concise way."
                prompt += self._language_instruction(language)
                return prompt

            case PromptTemplate.EXTRACT_ENTITIES:
                return (
                    "Extract the key entities from the following text. "
                    "Return the result strictly as a JSON object with key-value pairs. "
                    "Do not include explanations or extra text outside the JSON."
                )

            case _:
                raise ValueError(f"Unsupported prompt type: {self}")

    def _language_instruction(self, language: str) -> str:
        match language.lower():
            case "ita":
                return " The output langauage to use has to be Italian."
            case "eng":
                return " The output langauage to use has to be english."
            case "es":
                return " The output langauage to use has to be spanish."
            case "fr":
                return " The output langauage to use has to be franch."
            case _:
                raise ValueError(f"Unsupported language: {language}")
