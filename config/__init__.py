from os import environ as env

from pydantic import BaseModel, Field

from .database import DbConfig
from .server import ServerConfig


class Config(BaseModel):
    server: ServerConfig = Field(default_factory=lambda: ServerConfig(**env))
    database: DbConfig = Field(default_factory=lambda: DbConfig(**env))


config = Config()
