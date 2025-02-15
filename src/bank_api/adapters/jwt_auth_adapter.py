from datetime import datetime, timedelta

import jwt

from bank_api.ports.auth_adapter_interface import AuthAdapterInterface


class JWTAuthAdapter(AuthAdapterInterface):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, username: str, expires_in: int) -> str:
        payload = {
            'sub': username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
