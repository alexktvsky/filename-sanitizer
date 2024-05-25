import os
import re
import unicodedata
import unidecode


class FilenameSanitizer:
    def __init__(
        self, separator: str, replacements: list[str] = None,
        lowercase: bool = False, verbose: bool = True
    ) -> None:
        self._separator = separator
        self._replacements = replacements
        self._lowercase = lowercase
        self._verbose = verbose

    def process_path(self, path: str):
        # Extract the directory, base name, and extension from the file path
        dir_name, base_name = os.path.split(path)
        name, ext = os.path.splitext(base_name)

        # Create the new file name
        new_name = self._sanitize(name)
        new_file_name = f'{new_name}{ext}'
        new_path = os.path.join(dir_name, new_file_name)

        # Rename the file
        if path == new_path:
            return

        if os.path.exists(new_path):
            print(f'Failed to rename "{path}" because the file "{new_path}" already exists. Skipped')
            return

        os.rename(path, new_path)
        if self._verbose:
            print(f'"{path}" -> "{new_path}"')

    def process_directory(self, path: str):
        if not os.path.isdir(path):
            raise RuntimeError(f'"{path}" is not a directory')

        # First, process all files and directories in the directory
        for root, dirs, files in os.walk(path, topdown=False):
            # Process files first
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.process_path(file_path)

            # Process directories after processing files
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                self.process_path(dir_path)

    def _sanitize(self, text: str):
        if self._replacements:
            for old, new in self._replacements:
                text = text.replace(old, new)

        # Ensure text is unicode
        if not isinstance(text, str):
            text = str(text, 'utf-8', 'ignore')

        # Normalize text
        text = unicodedata.normalize('NFKD', text)

        # Transliterate non-ASCII characters into ASCII characters
        text = unidecode.unidecode(text)

        # Replace all other unwanted characters
        pattern = re.compile(r'[^-a-zA-Z0-9._]+')
        text = re.sub(pattern, self._separator, text)

        # Remove redundant separators
        pattern = re.compile(self._separator + r'{2,}')
        text = pattern.sub(self._separator, text)
        text = text.strip(self._separator)

        # Make the text lowercase (optional)
        if self._lowercase:
            text = text.lower()

        return text
