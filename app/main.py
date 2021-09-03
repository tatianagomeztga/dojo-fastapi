from fastapi import FastAPI

from app.db.config import server

app = FastAPI(title="Dojo FastAPI")


@app.on_event("startup")
async def startup_event():
    server(app)
