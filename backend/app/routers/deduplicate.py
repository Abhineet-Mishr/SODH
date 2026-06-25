from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..models.responses import DeduplicateResponse
from ..services.analytics import generate_counts
from ..services.artifact_manager import create_job, set_job_response, set_job_state
from ..services.cleanup import cleanup_expired_artifacts
from ..services.deduplicator import deduplicate_records
from ..services.parser import detect_source_type, normalize_imported_dataframe, parse_bytes
from ..services.normalizer import standardize_dataframe
from ..services.pipeline import build_dataset_exports, preview_records, public_artifact_payload
from ..utils.helpers import parse_artifact_lifetime_minutes, parse_fuzzy_threshold

router = APIRouter(prefix="/api/literature", tags=["deduplicate"])


def _standardize_file(filename: str, content: bytes) -> pd.DataFrame:
    source_type = detect_source_type(filename)
    dataframe = parse_bytes(filename, content)
    if dataframe.empty:
        return dataframe
    if source_type == "CSV":
        dataframe = normalize_imported_dataframe(dataframe)
    return standardize_dataframe(dataframe, source_database=Path(filename).stem, source_type=source_type)


@router.post("/deduplicate", response_model=DeduplicateResponse)
async def deduplicate_files(
    files: list[UploadFile] = File(...),
    artifact_lifetime_minutes: int = Form(30),
    fuzzy_threshold: int = Form(90),
):
    """Merge RIS/NBIB files, deduplicate them, and build screening exports."""
    cleanup_expired_artifacts()
    lifetime_minutes = parse_artifact_lifetime_minutes(artifact_lifetime_minutes)
    threshold = parse_fuzzy_threshold(fuzzy_threshold)

    if not files:
        raise HTTPException(status_code=400, detail="At least one file is required")

    seen_fingerprints: set[str] = set()
    frames: list[pd.DataFrame] = []
    source_counts: dict[str, int] = {}

    for uploaded in files:
        content = await uploaded.read()
        if not content:
            continue
        fingerprint = hashlib.sha256(uploaded.filename.encode("utf-8") + b"::" + content).hexdigest()
        if fingerprint in seen_fingerprints:
            continue
        seen_fingerprints.add(fingerprint)
        try:
            standardized = _standardize_file(uploaded.filename, content)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=f"{uploaded.filename}: {exc}") from exc
        if standardized.empty:
            continue
        source_counts[standardized["source_database"].iloc[0]] = source_counts.get(standardized["source_database"].iloc[0], 0) + len(standardized)
        frames.append(standardized)

    if not frames:
        raise HTTPException(status_code=400, detail="No records found")

    master_dataset = pd.concat(frames, ignore_index=True)
    if len(master_dataset) > 50_000:
        raise HTTPException(status_code=413, detail="Large file limit exceeded")

    dedupe_result = deduplicate_records(master_dataset, minimum_score=threshold)
    master_dataset = dedupe_result["master_dataset"]
    exact_title_dataset = dedupe_result["exact_title_dataset"]
    deduplicated_dataset = dedupe_result["deduplicated_dataset"]
    review_dataset = dedupe_result["review_dataset"]
    report = dedupe_result["report"]
    report.update(generate_counts(master_dataset, deduplicated_dataset))
    report["source_counts"] = source_counts

    job = create_job(pipeline_kind="deduplicate", artifact_lifetime_minutes=lifetime_minutes)
    set_job_state(
        job.job_id,
        master_dataset=master_dataset,
        exact_title_dataset=exact_title_dataset,
        deduplicated_dataset=deduplicated_dataset,
        review_dataset=review_dataset,
        report=report,
        source_counts=source_counts,
        finalized=False,
    )
    artifacts = build_dataset_exports(job.job_id, master_dataset, deduplicated_dataset, review_dataset, report, include_master=True)
    response = {
        "job_id": job.job_id,
        "preview": preview_records(deduplicated_dataset),
        "master_preview": preview_records(master_dataset),
        "review_preview": preview_records(review_dataset) if not review_dataset.empty else [],
        "report": report,
        "artifacts": public_artifact_payload(job.job_id, artifacts),
        "finalized": False,
    }
    set_job_response(job.job_id, response)
    return response
