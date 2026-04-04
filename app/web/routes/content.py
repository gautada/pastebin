from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse, PlainTextResponse

from app.infra.storage import get_path, get_record

router = APIRouter()


@router.get("/f/{blob_id}")
def download(blob_id: str):
    """
    Download the blob as a file attachment.
    """
    rec = get_record(blob_id)
    if not rec:
        return PlainTextResponse("Not found", status_code=404)

    path = get_path(rec)
    if not path.exists():
        return PlainTextResponse("Not found", status_code=404)

    # download as attachment
    return FileResponse(
        path,
        media_type=rec.content_type,
        filename=rec.original_name,
    )


@router.get("/c/{blob_id}")
def raw(blob_id: str):
    """
    Return the raw blob content with its original MIME type.
    """
    rec = get_record(blob_id)
    if not rec:
        return PlainTextResponse("Not found", status_code=404)

    path = get_path(rec)
    if not path.exists():
        return PlainTextResponse("Not found", status_code=404)

    return FileResponse(path, media_type=rec.content_type)
