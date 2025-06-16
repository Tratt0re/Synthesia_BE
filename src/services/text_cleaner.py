import logging
import re
from cleantext import clean
from src.core.architecture import Service


class TextCleaner(Service):
    def __init__(self):
        """
        Initializes the TextCleaner service with default cleaning options.
        """
        try:
            self.set_cleaning_options(
                fix_unicode=True,
                to_ascii=True,
                lower=True,
                no_urls=True,
                no_emails=True,
                no_phone_numbers=True,
                no_punct=True,
                no_digits=False,
                no_currency_symbols=True,
                no_emojis=True,
                replace_with_url="",
                replace_with_email="",
                replace_with_phone_number="",
                replace_with_punct="",
                replace_with_number="",
                replace_with_currency_symbol="",
            )
            logging.info("-- TextCleaner service initialized --")
        except Exception as err:
            logging.error(f"TextCleaner/__init__ - Failed to initialize: {err}")

    def set_cleaning_options(
        self,
        fix_unicode: bool = True,
        to_ascii: bool = True,
        lower: bool = True,
        no_urls: bool = True,
        no_emails: bool = True,
        no_phone_numbers: bool = True,
        no_punct: bool = True,
        no_digits: bool = False,
        no_currency_symbols: bool = True,
        no_emojis: bool = True,
        replace_with_url: str = "",
        replace_with_email: str = "",
        replace_with_phone_number: str = "",
        replace_with_punct: str = "",
        replace_with_number: str = "",
        replace_with_currency_symbol: str = "",
    ):
        """
        Sets the cleaning options for text processing.

        Args:
        - Various flags to control what to remove or replace in the text.
        """
        self.cleaning_options = {
            "fix_unicode": fix_unicode,
            "to_ascii": to_ascii,
            "lower": lower,
            "no_urls": no_urls,
            "no_emails": no_emails,
            "no_phone_numbers": no_phone_numbers,
            "no_punct": no_punct,
            "no_digits": no_digits,
            "no_currency_symbols": no_currency_symbols,
            "no_emoji": no_emojis,
            "replace_with_url": replace_with_url,
            "replace_with_email": replace_with_email,
            "replace_with_phone_number": replace_with_phone_number,
            "replace_with_punct": replace_with_punct,
            "replace_with_number": replace_with_number,
            "replace_with_currency_symbol": replace_with_currency_symbol,
        }

    def clean_text(self, text: str) -> str:
        """
        Cleans the input text based on the configured options.

        Args:
        - text: The input text to be cleaned.

        Returns:
        - The cleaned text as a string.
        """
        try:
            cleaned_text = clean(text, **self.cleaning_options)
            return cleaned_text
        except Exception as err:
            logging.error(f"TextCleaner/clean_text - Failed to clean text: {err}")
            return text

    def remove_html_tags(self, text: str) -> str:
        """
        Removes all HTML/XML tags from the input text.

        Args:
        - text: The text possibly containing HTML/XML tags.

        Returns:
        - Cleaned text without any tags.
        """
        try:
            cleaned_text = re.sub(r"<.*?>", "", text)
            return cleaned_text
        except Exception as err:
            logging.error(
                f"TextCleaner/remove_html_tags - Failed to remove tags: {err}"
            )
            return text
