class ReplaceTableItem:
    def __init__(self, from_substr: str, to_substr: str) -> None:
        self._from_substr = from_substr
        self._to_substr = to_substr

    @property
    def from_substr(self):
        return self._from_substr

    @property
    def to_substr(self):
        return self._to_substr
