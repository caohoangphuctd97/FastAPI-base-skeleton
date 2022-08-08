from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins.request_id import RequestIdPlugin
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware  # type: ignore  # noqa: E501


def configure_middlewares(app: FastAPI) -> None:
    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.add_middleware(RawContextMiddleware, plugins=(RequestIdPlugin(),))
