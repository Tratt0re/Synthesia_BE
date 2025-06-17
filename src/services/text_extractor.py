import logging
from fastapi import UploadFile
import tempfile
import pdfplumber
from src.core.architecture import Service


class TextExtractor(Service):
    def __init__(self):
        logging.info("-- TextExtractor service initialized --")

    async def extract_text(self, file: UploadFile) -> str:
        try:
            filename = file.filename.lower()

            if filename.endswith(".txt"):
                content = await file.read()
                return content.decode("utf-8")

            elif filename.endswith(".pdf"):
                return await self._extract_pdf_text(file)

            else:
                raise ValueError("Unsupported file type")

        except Exception as e:
            logging.error(f"[TextExtractorService] extract_text() failed: {e}")
            raise

    async def _extract_pdf_text(self, file: UploadFile) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        with pdfplumber.open(tmp_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
