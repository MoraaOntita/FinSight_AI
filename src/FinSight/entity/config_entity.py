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
class DataStorageConfig:
    root_dir: Path
    db_url: str
    table_name: str

@dataclass(frozen=True)
class DBConnectionConfig:
    db_url: str