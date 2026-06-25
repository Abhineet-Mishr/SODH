from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from ..parser import detect_source_type, normalize_imported_dataframe, parse_bytes


def parse_upload(filename: str, content: bytes) -> tuple[str, pd.DataFrame]:
    """Parse an uploaded file and return the detected source type plus dataframe."""
    source_type = detect_source_type(filename)
    dataframe = parse_bytes(filename, content)
    return source_type, dataframe


def parse_source_database(filename: str) -> str:
    return Path(filename).stem


__all__ = ["detect_source_type", "normalize_imported_dataframe", "parse_bytes", "parse_upload", "parse_source_database"]

