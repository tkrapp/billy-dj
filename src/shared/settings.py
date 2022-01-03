from pathlib import Path
from zero_settings import ZeroSettings

app_settings = ZeroSettings(
    key="SHARED",
    defaults={
        "POSTAL_CODES_TRIE_FILE": Path(__file__).parent / "resources" / "postal_codes.marisa"
    }
)
