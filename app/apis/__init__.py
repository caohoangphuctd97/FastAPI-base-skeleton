from . import customers, health, devices
from fastapi import FastAPI
from app.config import config

def configure_routes(app: FastAPI):
    app.include_router(router=health.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=customers.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=devices.router, prefix=config.OPENAPI_PREFIX)
