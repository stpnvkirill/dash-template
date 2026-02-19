from pydantic import BaseModel


class ServerConfig(BaseModel):
    SECRET_KEY: str
    LRU_CACHE_MAXSIZE: int = 0
