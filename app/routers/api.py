from fastapi import APIRouter

from app.routers.db import user
from app.routers.external import socket

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["user"])
router.include_router(socket.router, prefix="/web-socket", tags=["ws"])
