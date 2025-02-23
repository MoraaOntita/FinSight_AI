from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataFetchConfig:
    root_dir: Path
    ticker: str
    start_date: str
    end_date: str
    period: str
    output_file: Path

@dataclass(frozen=True)
class DataStorageConfig:  # ✅ Add this class
    root_dir: Path
    db_url: str
    table_name: str
