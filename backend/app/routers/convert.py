from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..models.requests import ConversionType
from ..services.artifact_manager import create_job, serialize_artifact, set_job_response, store_artifact
from ..services.cleanup import cleanup_expired_artifacts
from ..services.exporter import dataframe_to_csv_bytes, dataframe_to_nbib_bytes, dataframe_to_ris_bytes
from ..services.normalizer import standardize_dataframe
from ..services.parser import normalize_imported_dataframe, parse_upload, parse_source_database
from ..services.pipeline import preview_records

router = APIRouter(prefix="/api/literature", tags=["convert"])


@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    conversion: ConversionType = Form(...),
    artifact_lifetime_minutes: int = Form(30),
):
    """Convert one literature file between RIS, NBIB, and CSV."""
    cleanup_expired_artifacts()

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty upload")

    try:
        source_type, dataframe = parse_upload(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if dataframe.empty:
        raise HTTPException(status_code=400, detail="No records found")

    if source_type == "CSV":
        dataframe = normalize_imported_dataframe(dataframe)

    standardized = standardize_dataframe(dataframe, source_database=parse_source_database(file.filename), source_type=source_type)
    output_dataframe = standardized.drop(columns=["normalized_title", "source_type", "record_index"], errors="ignore")

    if conversion.endswith("_TO_CSV"):
        output_filename = Path(file.filename).with_suffix(".csv").name
        output_bytes = dataframe_to_csv_bytes(output_dataframe)
        mime_type = "text/csv"
    elif conversion.endswith("RIS"):
        output_filename = Path(file.filename).with_suffix(".ris").name
        output_bytes = dataframe_to_ris_bytes(output_dataframe)
        mime_type = "application/x-research-info-systems"
    else:
        output_filename = Path(file.filename).with_suffix(".nbib").name
        output_bytes = dataframe_to_nbib_bytes(output_dataframe)
        mime_type = "application/octet-stream"

    job = create_job(pipeline_kind="convert", artifact_lifetime_minutes=artifact_lifetime_minutes)
    artifact = store_artifact(job.job_id, "converted_file", output_filename, output_bytes, mime_type)
    public_artifact = serialize_artifact(job.job_id, artifact)
    response = {
        "job_id": job.job_id,
        "source_type": source_type,
        "conversion": conversion,
        "records": int(len(standardized)),
        "preview": preview_records(output_dataframe),
        "download_name": output_filename,
        "artifact": public_artifact,
        "download_url": public_artifact["download_url"],
    }
    set_job_response(job.job_id, response)
    return response
