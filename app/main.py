from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.web.routes.content import router as content_router
from app.web.routes.home import router as home_router
from app.web.routes.query import router as query_router
from app.web.routes.upload import router as upload_router
from app.web.routes.view import router as view_router

# Default: Maybe move app/fastapi to this structure
# def main():
#     print("Hello from pastebin!")
#
#
# if __name__ == "__main__":
#     main()
#


def create_app() -> FastAPI:
    app = FastAPI(title="myapp")

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # *** REGISTER ROUTERS ***
    # GET "/" home/index.html
    app.include_router(home_router)
    # GET "/c/{id} raw blob as file"
    app.include_router(content_router)
    # GET "/q JSON"
    app.include_router(query_router)
    # GET "/v/{id} page or card"
    app.include_router(view_router)

    # POST "/u"
    app.include_router(upload_router)

    return app


app = create_app()
templates = Jinja2Templates(directory="app/templates")
