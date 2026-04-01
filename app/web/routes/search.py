from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse

from app.infra.storage import search_records
from app.web.templating import templates

router = APIRouter()


@router.get("/search", response_class=HTMLResponse)
def search(request: Request, q: str = Query("", min_length=0)):
    term = q.strip()
    results = search_records(term) if term else []
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "title": "Search",
            "query": term,
            "results": results,
        },
    )
