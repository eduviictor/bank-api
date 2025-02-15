from pydantic import BaseModel


class AuthInput(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
