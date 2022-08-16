import json
import logging
import re
from typing import Dict
from redis import Redis

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.exceptions.configure_exceptions import (
    InvalidPassword, WrongCredentialsException, ServerErrorException
)
from app.config import config
from app.utils.jwt import redis_conn

logger = logging.getLogger(__name__)
oauth2_scheme = HTTPBearer(auto_error=False)


class PasswordHandle:

    @property
    def pwd_context(self):
        return CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    @staticmethod
    def validate_password(password):
        regex_pattern = "(?=.{8,}).*$"
        if not re.match(regex_pattern, password):
            raise InvalidPassword("invalidPassword")

    def verify_password(self, plain_password, hashed_password):
        try:
            verify = False
            if plain_password is not None and hashed_password is not None:
                verify = self.pwd_context.verify(
                    secret=plain_password,
                    hash=hashed_password
                )
        except UnknownHashError:
            raise WrongCredentialsException("password")
        if not verify:
            raise WrongCredentialsException("password")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)


def create_auth_tokens(
    authorize: AuthJWT, subject: str, redis_db: Redis, claims: Dict
):
    access_expires_time = config.jwt.authjwt_access_token_expires
    refresh_token = authorize.create_refresh_token(
        subject=subject,
        user_claims=claims,
        expires_time=False
    )
    access_token = authorize.create_access_token(
        subject=subject,
        user_claims=claims,
        expires_time=access_expires_time
    )
    redis_login(authorize, redis_db, access_token, refresh_token)
    return access_token, refresh_token


def refresh_access_token(authorize, redis_db, sub, claims):
    auth_jwt = AuthJWT()
    access_expires_time = config.jwt.authjwt_access_token_expires
    access_token = auth_jwt.create_access_token(
        subject=sub,
        user_claims=claims,
        expires_time=access_expires_time
    )
    redis_update_refresh_for_access_token(
        authorize=auth_jwt,
        access_expires_time=access_expires_time,
        access_token=access_token,
        refresh_jti=authorize['jti'],
        redis_db=redis_db
    )
    return access_token


def check_existing_jwt_token(raw_jwt):
    entry = redis_conn.get(generate_key_auth_token(raw_jwt))
    return entry is not None


def verify_access_token(authorize: AuthJWT, sub: str):
    try:
        authorize.jwt_required()
        raw_jwt = authorize.get_raw_jwt()
        if authorize.get_jwt_subject() == sub and \
           check_existing_jwt_token(raw_jwt):
            return raw_jwt
    except Exception as e:
        logger.info(e)
    raise ServerErrorException("Wrong Token")


def customer_claims(**kwargs):
    return {
        "email": kwargs.get('email', None),
        "phone": kwargs.get('phone', None),
        "first_name": kwargs.get('first_name', None),
        "last_name": kwargs.get('last_name', None),
        "customer_id": kwargs.get('customer_id', None)
    }


def redis_login(
    authorize: AuthJWT, redis_db: Redis, access_token=None, refresh_token=None
):
    try:
        if access_token is not None:
            data: Dict = {}
            raw_jwt_access = authorize.get_raw_jwt(access_token)
            if refresh_token is not None:
                raw_jwt_refresh = authorize.get_raw_jwt(refresh_token)
                redis_db.set(
                    generate_key_auth_token(raw_jwt_refresh),
                    json.dumps(data)
                )
                data['jwt_refresh'] = raw_jwt_refresh['jti']
            if "exp" in raw_jwt_access:
                redis_db.setex(
                    generate_key_auth_token(raw_jwt_access),
                    config.jwt.authjwt_access_token_expires,    # type: ignore
                    json.dumps(data)
                )
            else:
                redis_db.set(
                    generate_key_auth_token(raw_jwt_access),
                    json.dumps(data)
                )

    except Exception as e:
        logger.error(e)
        raise ServerErrorException("Redis Error")


def redis_update_refresh_for_access_token(
    authorize: AuthJWT,
    access_token: str,
    access_expires_time: int,
    refresh_jti: str,
    redis_db: Redis
):
    try:
        raw_jwt_access = authorize.get_raw_jwt(access_token)
        data = {
            'jwt_refresh': refresh_jti
        }
        redis_db.setex(
            generate_key_auth_token(raw_jwt_access),
            access_expires_time,
            json.dumps(data)
        )
    except Exception as e:
        logger.error(e)
        raise ServerErrorException("Refresh Token Error")


def depend_customer_access_token(
    authorize: AuthJWT = Depends(),
    _oauth2_schema: str = Depends(oauth2_scheme)
):
    return verify_access_token(authorize, "customer")


def generate_key_auth_token(raw_jwt):
    sub = raw_jwt['sub']
    instance_id = raw_jwt[f"{sub}_id"]
    return f"/{config.redis.redis_prefix}/auth/{sub}/{instance_id}/{raw_jwt['type']}_token/{raw_jwt['jti']}"    # noqa: E501
