# SODH Literature Toolkit Backend

This FastAPI service powers the literature conversion and deduplication workflows.

## Modules

- `app_factory.py` — application wiring and startup cleanup
- `routers/convert.py` — file conversion endpoint
- `routers/deduplicate.py` — merge and deduplication endpoint
- `routers/review.py` — review persistence, threshold recomputation, finalize
- `routers/download.py` — artifact downloads
- `services/artifact_manager.py` — in-memory job and artifact registry
- `services/pipeline.py` — export bundle assembly and previews
- `services/parser.py` — RIS, NBIB, and CSV ingestion
- `services/normalizer.py` — standard schema mapping and title normalization
- `services/deduplicator.py` — DOI, PMID, exact-title, and fuzzy deduplication
- `services/exporter.py` — CSV and Excel exports
- `services/analytics.py` — summary statistics and PRISMA-style counts

## Run

```bash
uvicorn backend.app.main:app --reload
```

## Notes

- Temporary artifacts are written to `tmp/`
- Processing logs are written to `logs/literature_toolkit.log`
- The module is intentionally isolated so it can later be mounted inside Synapse
- Artifact lifetime cleanup runs on startup and before convert/deduplicate jobs
