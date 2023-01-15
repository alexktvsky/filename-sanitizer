from typing import List

from filename_sanitizer.replace_table_item import ReplaceTableItem


class Replacer:

    _builtin_table: List[ReplaceTableItem] = []

    def __init__(
        self,
        additional_table: List[ReplaceTableItem] = None
    ) -> None:
        self._additional_table = additional_table

    def replace_all(self, name: str) -> str:
        for table_item in self._builtin_table:
            name = name.replace(table_item.from_substr, table_item.to_substr)

        if self._additional_table is not None:
            for table_item in self._additional_table:
                name = name.replace(table_item.from_substr, table_item.to_substr)

        return name
