from .base import AppError
from .user import UserIsAuthenticated, UserNotAuthenticated


def error_handler(err):
    if issubclass(err.__class__, AppError):
        return err.on_error()
    else:
        raise err
