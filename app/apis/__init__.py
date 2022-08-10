from . import customers, health, devices
from fastapi import FastAPI


def configure_routes(app: FastAPI):
    app.include_router(router=health.router, prefix="/api")
    app.include_router(router=customers.router, prefix="/api")
    app.include_router(router=devices.router, prefix="/api")
