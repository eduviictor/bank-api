from typing import Dict, Optional

import jwt
from fastapi import Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.utils.log import logger
from settings import SECRET_KEY


class JWTBearerMiddleware(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[Dict]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HttpException(
                    code=status.HTTP_403_FORBIDDEN,
                    message='Invalid authentication scheme.'
                )
            payload = self.__validate_token(credentials.credentials)
            if not payload:
                raise HttpException(
                    code=status.HTTP_403_FORBIDDEN,
                    message='Invalid authorization code.'
                )
            return payload
        else:
            raise HttpException(
                code=status.HTTP_403_FORBIDDEN,
                message='Invalid authorization code.'
            )

    def __validate_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.info('Token expirado')
            return None
        except jwt.InvalidTokenError:
            logger.info('Token inválido')
            return None

jwt_bearer_middleware = JWTBearerMiddleware()
