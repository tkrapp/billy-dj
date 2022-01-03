import json
from pathlib import Path
from typing import Optional, Sequence, TextIO, Tuple, cast
from django.core.exceptions import ImproperlyConfigured

from marisa_trie import BytesTrie

from ..settings import app_settings


def generate_trie(input_file: TextIO) -> BytesTrie:
    input_data = json.load(input_file)

    return BytesTrie(
        (row["zipcode"], row["city"].encode()) for row in input_data.values()
    )


class PostalCodeIndex:
    def __init__(self, index_file: Optional[Path]):
        self._index = BytesTrie()
        self._index_file = index_file
        self._index_loaded = False

    def _load_index(self):
        if self._index_file is None:
            self._index_loaded = True
            return

        if not self._index_file.exists():
            raise ImproperlyConfigured(f"File {trie_file} does not exists")
        elif not self._index_file.is_file():
            raise ImproperlyConfigured(f"{trie_file} is not a file")

        self._index.load(str(self._index_file))
        self._index_loaded = True

    def search(self, postal_code: str) -> Sequence[Tuple[str, bytes]]:
        if not self._index_loaded:
            self._load_index()

        return self._index.items(postal_code)


trie_file = Path()
postal_code_index = PostalCodeIndex(cast(Path, app_settings.POSTAL_CODES_TRIE_FILE))
