# SODH Literature Toolkit

Standalone literature management module for conversion, merging, deduplication, and screening exports.

## Layout

- `backend/` — FastAPI service and literature processing modules
- `frontend/` — React + TypeScript + Tailwind UI

## Backend Structure

- `backend/app/main.py` — application entrypoint only
- `backend/app/app_factory.py` — app setup, routers, startup cleanup, exception handling
- `backend/app/routers/` — convert, deduplicate, review, and download endpoints
- `backend/app/services/` — parsing, deduplication, export, artifact management, cleanup, analytics
- `backend/app/models/` — typed request and response schemas
- `backend/app/utils/` — shared helpers and normalization utilities

## Run locally

1. Start the backend from the repo root:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

2. Start the frontend from `frontend/`:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Exports

- Master dataset CSV
- Deduplicated CSV
- Deduplicated Excel workbook
- Duplicate review sheet
- Processing report
- Screening-ready Excel workbook

## Processing Settings

- Artifact lifetime: 30 min, 1 hr, 2 hr, 3 hr, 6 hr, 12 hr, 24 hr
- Duplicate sensitivity: Conservative, Balanced, Aggressive, or Custom 85%–99%

## Logging

- Processing events are written to `logs/literature_toolkit.log`
- Temporary artifacts are stored under `tmp/`

## Backend modules

- `backend/app/parser.py`
- `backend/app/normalizer.py`
- `backend/app/deduplicator.py`
- `backend/app/exporter.py`
- `backend/app/analytics.py`

## Workflow

1. Upload literature exports
2. Parse and normalize metadata
3. Merge records from all sources
4. Deduplicate by DOI, PMID, exact title, and fuzzy title
5. Review duplicates
6. Download CSV, Excel, and report artifacts
