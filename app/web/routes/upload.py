"""
upload.py - FastAPI route for file upload endpoint

This module provides the /u endpoint for uploading files to the server. Uploaded files
are saved using the storage layer, and metadata about each upload is returned in the
response. The endpoint supports multiple file uploads in a single request.
"""

from pathlib import Path
from typing import List

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse

from app.infra.storage import save_bytes

# Create a router for upload endpoints
router = APIRouter()

# Directory for storing uploaded files (legacy, not used in v2)
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/u")
async def upload(request: Request, files: List[UploadFile] = File(...)):
    """
    Upload one or more files to the server.

    Args:
        request (Request): The incoming HTTP request (used for base URL).
        files (List[UploadFile]): List of files to upload (multipart/form-data).

    Returns:
        JSONResponse: A response containing metadata for each uploaded file, including:
            - id: Unique identifier for the file
            - original_name: Original filename
            - bytes: File size in bytes
            - content_type: MIME type
            - view_url: URL to view the file
            - download_url: URL to download the file
    """
    saved = []
    base = str(request.base_url).rstrip("/")  # e.g. http://127.0.0.1:8000
    for f in files:
        # Read file content
        content = await f.read()
        # Save file using storage layer
        rec = save_bytes(f.filename or "upload", content, f.content_type)

        # Collect metadata for response
        saved.append(
            {
                "id": rec.id,
                "original_name": rec.original_name,
                "bytes": rec.bytes,
                "content_type": rec.content_type,
                "view_url": f"{base}/v/{rec.id}",
                "download_url": f"{base}/f/{rec.id}",
            }
        )
        print(saved)  # Debug: print saved metadata
    return JSONResponse({"ok": True, "saved": saved})
