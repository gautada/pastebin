# REMOVE THE PASTE BACKEND
# TODO: This is to be the full page view and the card view for content


# from __future__ import annotations
#
# from datetime import datetime
#
# from fastapi import APIRouter, Form, Request
# from fastapi.responses import JSONResponse
#
# from app.infra.storage import save_bytes
#
# router = APIRouter()
#
#
# @router.post("/paste")
# async def paste_text(
#     request: Request,
#     content: str = Form(...),  # noqa: B008
#     language: str = Form("plaintext"),  # noqa: B008
# ):
#     # language: str = Form("plaintext"), optional; used for highlighting
#     # store as .txt
#     name = f"paste-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.txt"
#     rec = save_bytes(name, content.encode("utf-8"), "text/plain")
#
#     base = str(request.base_url).rstrip("/")
#     return JSONResponse(
#         {
#             "ok": True,
#             "id": rec.id,
#             "view_url": f"{base}/p/{rec.id}?lang={language}",
#             "download_url": f"{base}/f/{rec.id}",
#         }
#     )

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
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


@router.get("/v/{blob_id}", response_class=HTMLResponse)
def view(blob_id: str, request: Request):

    rec = get_record(blob_id)
    if not rec:
        return PlainTextResponse("Record not found", status_code=404)

    path = get_path(rec)
    if not path.exists():
        return PlainTextResponse("Path Not found", status_code=404)

    inline_text = None
    is_text = (
        rec.content_type.startswith("text/") or rec.content_type in TEXT_TYPES
    )  # noqa: E501

    if is_text and rec.bytes <= MAX_INLINE_BYTES:
        try:
            inline_text = path.read_text("utf-8", errors="replace")
        except Exception:
            inline_text = None

    # allow `?lang=python` etc.
    lang = request.query_params.get("lang", "plaintext")
    return templates.TemplateResponse(
        "view.html",
        {
            "request": request,
            "title": f"Paste {blob_id}",
            "rec": rec,
            "inline_text": inline_text,
            "lang": lang,
        },
    )


# @router.get("/f/{blob_id}")
# def download(blob_id: str):
#     rec = get_record(blob_id)
#     if not rec:
#         return PlainTextResponse("Not found", status_code=404)
#
#     path = get_path(rec)
#     if not path.exists():
#         return PlainTextResponse("Not found", status_code=404)
#
#     # download as attachment
#     return FileResponse(
#         path,
#         media_type=rec.content_type,
#         filename=rec.original_name,
#     )
