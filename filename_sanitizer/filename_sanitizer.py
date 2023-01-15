from typing import List

from filename_sanitizer.replace_table_item import ReplaceTableItem
from filename_sanitizer.transliter import Transliter
from filename_sanitizer.transliter import LanguageDetectionError
from filename_sanitizer.replacer import Replacer


class FilenameSanitizer:
    def __init__(
        self,
        table: List[ReplaceTableItem] = None,
        to_lower: bool = False,
    ) -> None:
        self._transliter = Transliter()
        self._to_lower = to_lower
        self._replacer = Replacer(table)

    def sanitize(self, filename: str) -> str:

        # Replace multiple spaces with a single space
        sanitized_name = ' '.join(filename.split())

        try:
            sanitized_name = self._transliter.translit(sanitized_name)
        except LanguageDetectionError:
            pass

        if self._to_lower:
            sanitized_name = sanitized_name.lower()


        sanitized_name = self._replacer.replace_all(sanitized_name)

        return sanitized_name
