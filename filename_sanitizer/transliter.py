import transliterate


LanguageDetectionError = transliterate.exceptions.LanguageDetectionError


class Transliter:
    def translit(self, text: str, src: str = None) -> str:
        return transliterate.translit(text, language_code=src, reversed=True)
