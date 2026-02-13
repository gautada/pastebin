"""
status.py - FastAPI route for /status endpoint

This endpoint returns a JSON list of the 5 most recent blobs uploaded to the
system. Blobs are retrieved from the storage index and sorted by insertion
order (most recent first).
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.infra.storage import _load_index

# Create a router for status endpoints
router = APIRouter()


# @TO-DO: Add general queries like columns , etc currently this is just the
# latest
@router.get("/query")
async def query():
    """
    Get the 5 most recent blobs uploaded.

    Returns:
        JSONResponse: List of the 5 most recent blob records (most recent
        first).
    """
    idx = _load_index()
    print(idx)
    # Get the last 5 blobs by insertion order (Python 3.7+ dicts preserve order)
    latest = list(idx.values())[-5:][::-1]  # last 5, most recent first
    return JSONResponse(latest)
