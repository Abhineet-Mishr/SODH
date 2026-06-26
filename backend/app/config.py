from __future__ import annotations

from pathlib import Path


APP_NAME = "SODH Literature Toolkit"
API_PREFIX = "/api/literature"

BASE_DIR = Path(__file__).resolve().parents[2]
TEMP_DIR = BASE_DIR / "tmp"
LOG_DIR = BASE_DIR / "logs"

MAX_UPLOAD_RECORDS = 50_000
PREVIEW_ROWS = 20
FUZZY_THRESHOLD_HIGH = 98
FUZZY_THRESHOLD_LIKELY = 95
FUZZY_THRESHOLD_POSSIBLE = 90

STANDARD_FIELDS = [
    "title",
    "authors",
    "year",
    "journal",
    "doi",
    "abstract",
    "keywords",
    "pmid",
    "source_database",
]

SCREENING_COLUMNS = [
    "Title",
    "Authors",
    "Year",
    "Journal",
    "DOI",
    "PMID",
    "Abstract",
    "Keywords",
    "Database Source",
    "Include",
    "Exclude",
    "Maybe",
    "Reason for Exclusion",
    "Reviewer",
    "Notes",
]
