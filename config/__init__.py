from os import environ as env

from pydantic import BaseModel, Field

from .server import ServerConfig


class Config(BaseModel):
    server: ServerConfig = Field(default_factory=lambda: ServerConfig(**env))


config = Config()
