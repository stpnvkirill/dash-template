from pydantic import BaseModel


class ServerConfig(BaseModel):
    """Server configuration.

    Attributes:
        SECRET_KEY: Flask secret key.
        LRU_CACHE_MAXSIZE: Max size for LRU caches (0 = unlimited, default: 100).
    """

    SECRET_KEY: str
    LRU_CACHE_MAXSIZE: int = 100  # Default to 100 for better caching
