# import os

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from starlette.responses import HTMLResponse

from .__version__ import __version__
from .config import config
from .exceptions import configure_exceptions_handlers
from .middlewares import configure_middlewares
from .configure_logging import configure_logging

from app.apis import configure_routes


# Create instance of application
app = FastAPI(
    title=config.APPLICATION_NAME,
    description=config.DESCRIPTION,
    version=__version__,
    debug=config.DEBUG,
    openapi_url=f"{config.OPENAPI_PREFIX}/openapi.json",
    docs_url=None,
    redoc_url=f"{config.OPENAPI_PREFIX}/doc",
)
# Update and set up configs
configure_logging(log_level=config.LOG_LEVEL)
configure_exceptions_handlers(app)
configure_middlewares(app)

# Configure routes and add dependencies
configure_routes(app)
# configure_routes(
#     app, modules=(saansook,),
#     prefix=config.OPENAPI_PREFIX,
#     dependencies=[
#         Depends(Authentication(config.auth0))
#     ]
# )


# For local testing
# @app.on_event('startup')
# async def create_database():
#     from .database.config import async_engine
#     from .database.models import BaseModel

#     async with async_engine.begin() as conn:
#         # Change `create_all` to `drop_all` to drop all tables
#         await conn.run_sync(BaseModel.metadata.create_all)


@app.router.get(f"{config.OPENAPI_PREFIX}", include_in_schema=False,
                response_class=HTMLResponse)
async def swagger_html():
    return get_swagger_ui_html(
        openapi_url=f"{config.OPENAPI_PREFIX}/swagger.json",
        title=app.title)


@app.router.get(
    f"{config.OPENAPI_PREFIX}/swagger.json",
    include_in_schema=False, response_class=UJSONResponse
)
async def custom_openapi_json():
    return custom_openapi()


def custom_openapi():
    openapi_schema = get_openapi(
        title=app.title, version=app.version,
        description=config.DESCRIPTION, routes=app.routes
    )
    return openapi_schema
