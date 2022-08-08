from . import health, saansook
from fastapi import FastAPI


def configure_routes(app: FastAPI):
    app.include_router(router=health.router, prefix="/api")
    app.include_router(router=saansook.router, prefix="/api")
