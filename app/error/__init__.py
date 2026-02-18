import logging

from .base import AppError
from .user import UserIsAuthenticated, UserNotAuthenticated


def error_handler(err):
    if issubclass(err.__class__, AppError):
        return err.on_error()
    else:
        logging.error(f"Unhandled exception: {err!s}", exc_info=err)
        raise err
