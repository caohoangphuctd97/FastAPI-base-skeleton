from typing import Literal, Optional
from pydantic import BaseSettings, validator
from pydantic.networks import PostgresDsn

DEFAULT_API_PREFIX = "api"
DEFAULT_API_VERSION = "v1beta1"


class AsyncPostgresDsn(PostgresDsn):
    default_scheme = "postgresql+asyncpg"
    allowed_schemes = {"postgresql+asyncpg", "postgres+asyncpg"}


class DatabaseServiceConfig(BaseSettings):
    DATABASE_URI: PostgresDsn

    DATABASE_POOL_SIZE: int = 2
    DATABASE_POOL_MAX: int = 10
    DATABASE_POOL_TIMEOUT: int = 10

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict:
        engine_option = {
            "pool_timeout": self.DATABASE_POOL_TIMEOUT,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_POOL_MAX,
        }

        return engine_option

    @property
    def ASYNC_DATABASE_URI(self) -> AsyncPostgresDsn:
        dsn = self.DATABASE_URI
        url = AsyncPostgresDsn(
            None,
            scheme=AsyncPostgresDsn.default_scheme,
            user=dsn.user,
            password=dsn.password,
            host=dsn.host,
            port=dsn.port,
            path=dsn.path,
        )
        return url


class PagingConfig(BaseSettings):
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 100
    MIN_PAGE: int = 1
    MIN_PAGE_SIZE: int = 1
    MAX_PAGE_SIZE: int = 1000
    PAGE_KEY: str = "page"
    PER_PAGE_KEY: str = "per_page"
    LINK_HEADER: str = "Link"
    PAGE_COUNT_HEADER: str = "X-Page-Count"
    TOTAL_COUNT_HEADER: str = "X-Total-Count"


class RedisSetting(BaseSettings):
    redis_host: str
    redis_port: str
    redis_prefix: str = "api"


class JWTSetting(BaseSettings):
    authjwt_secret_key: Optional[str] = "MY_SECRET"
    authjwt_algorithm: Optional[str] = "HS256"
    authjwt_access_token_expires: Optional[int] = 900
    authjwt_refresh_token_expires: Optional[int] = 86400


class Config(BaseSettings):
    APPLICATION_NAME = "SaanSook API"
    DESCRIPTION = "SaanSook API"

    ENVIRONMENT: Literal["dev", "qa", "prod"] = "dev"
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] \
        = "INFO"

    API_PREFIX: str = DEFAULT_API_PREFIX
    API_VERSION: str = DEFAULT_API_VERSION

    db = DatabaseServiceConfig()
    paging = PagingConfig()
    redis = RedisSetting()
    jwt = JWTSetting()

    @property
    def OPENAPI_PREFIX(self) -> str:
        return f"/{self.API_PREFIX}/{self.API_VERSION}"

    @validator("ENVIRONMENT")
    def _lowercase_environment(cls, v):
        return v.lower() if isinstance(v, str) else v

    @validator("LOG_LEVEL", pre=True)
    def _debug_log_level(cls, v, values, **kwargs):
        if values.get("DEBUG"):
            return "DEBUG"
        return v.upper()


config = Config()
