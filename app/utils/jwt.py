from fastapi_jwt_auth import AuthJWT

from app.utils.get_db import get_redis_db
from app.config import JWTSetting

redis_conn = get_redis_db()


@AuthJWT.load_config
def get_config():
    return JWTSetting()
