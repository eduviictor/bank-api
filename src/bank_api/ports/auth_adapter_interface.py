from abc import ABC


class AuthAdapterInterface(ABC):
    def generate_token(self, username: str, expires_in: int) -> str:
        pass
