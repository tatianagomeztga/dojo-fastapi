from typing import List

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates/")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(f"yo-{websocket.client.port}-{message}")

    async def broadcast(self, message: str, client_port):
        for connection in self.active_connections:
            if (connection.client.port != client_port): 
                await connection.send_text(f"otro-{client_port}-{message}")


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("chat/FastAPI-CHAT.html", context={'request': request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Entrando...", websocket.client.port)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{data}", websocket)
            await manager.broadcast(f"{data}", websocket.client.port)
    except Exception:
        manager.disconnect(websocket)
        await manager.broadcast(f"Saliendo...", websocket.client.port)