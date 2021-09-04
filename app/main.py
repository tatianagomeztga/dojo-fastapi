from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.config import server
from app.routers.api import router

app = FastAPI(title="Dojo FastAPI")
templates = Jinja2Templates(directory="app/templates")
app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(
        "chat/FastAPI-CHAT.html", context={"request": request}
    )


app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    server(app)
