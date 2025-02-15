from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from .base import ORMBaseModel


class User(ORMBaseModel):
    __tablename__ = 'user'  # type: ignore[assignment]

    username = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
