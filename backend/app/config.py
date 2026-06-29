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

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FEATURE_A_CREDITS = int(os.getenv("FEATURE_A_CREDITS", "5"))

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/sodh.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-that-should-be-changed")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
