from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse, PlainTextResponse
from starlette.templating import Jinja2Templates

from app.infra.storage import get_path, get_record

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

TEXT_TYPES = {
    "text/plain",
    "application/json",
    "application/xml",
    "text/html",
    "text/css",
    "text/javascript",
}

MAX_INLINE_BYTES = 200_000  # don’t try to render huge blobs inline

# @router.get("/c/{blob_id}", response_class=HTMLResponse)
# def view(blob_id: str, request: Request):
#     rec = get_record(blob_id)
#     if not rec:
#         return PlainTextResponse("Not found", status_code=404)
#
#     path = get_path(rec)
#     if not path.exists():
#         return PlainTextResponse("Not found", status_code=404)
#
#     inline_text = None
#     is_text = (
#         rec.content_type.startswith("text/") or rec.content_type in TEXT_TYPES
#     )  # noqa: E501
#
#     if is_text and rec.bytes <= MAX_INLINE_BYTES:
#         try:
#             inline_text = path.read_text("utf-8", errors="replace")
#         except Exception:
#             inline_text = None
#
#     # allow `?lang=python` etc.
#     lang = request.query_params.get("lang", "plaintext")
#     return templates.TemplateResponse(
#         "paste/view.html",
#         {
#             "request": request,
#             "title": f"Paste {blob_id}",
#             "rec": rec,
#             "inline_text": inline_text,
#             "lang": lang,
#         },
#     )

# TO-DO: This is the raw content it should return the blob as a file.


@router.get("/c/{blob_id}")
def download(blob_id: str):
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
