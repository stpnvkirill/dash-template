from pydantic import BaseModel


class ServerConfig(BaseModel):
    SECRET_KEY: str = "super_secret_key"
    LRU_CACHE_MAXSIZE: int = 128
