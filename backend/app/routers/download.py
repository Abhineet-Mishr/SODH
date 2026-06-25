from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..services.artifact_manager import get_job, resolve_download, tombstone_message

router = APIRouter(prefix="/api/literature", tags=["download"])


@router.get("/download/{job_id}/{artifact_id}")
def download_artifact(job_id: str, artifact_id: str) -> FileResponse:
    """Stream a previously generated artifact back to the client."""
    state, artifact = resolve_download(job_id, artifact_id)
    if state == "expired":
        raise HTTPException(status_code=410, detail=tombstone_message(job_id) or "Download expired")
    if state == "deleted" or not artifact:
        job = get_job(job_id)
        if job:
            raise HTTPException(status_code=404, detail="Artifact deleted")
        raise HTTPException(status_code=404, detail="Job not found")
    return FileResponse(artifact.path, filename=artifact.filename, media_type=artifact.mime_type)
