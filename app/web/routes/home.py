from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# Fixing dues to circular logic error
# from app.main import templates
from app.web.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Upload"},
    )
