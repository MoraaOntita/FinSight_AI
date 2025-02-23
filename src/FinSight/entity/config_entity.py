from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataFetchConfig:
    root_dir: Path
    ticker: str
    period: str
    start_date: str
    end_date: str
    output_file: Path
